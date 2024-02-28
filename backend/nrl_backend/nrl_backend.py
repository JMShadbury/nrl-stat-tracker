import aws_cdk as cdk
from constructs import Construct

file = open("../application_whitelist/whitelist.txt", "r")
allowed_ips = file.readlines()
file.close()

domain = "nrl.shadbury.com"
zone = "shadbury.com"
lb_port = 443
ecs_port = 80

environment = {
    "FLASK_ENV": "production",
    "FLASK_APP": "app.py"
}

class FlaskFargateStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = cdk.aws_ec2.Vpc(self, "NRL_VPC", max_azs=2)

        cluster = cdk.aws_ecs.Cluster(self, "NRL_CLUSTER", vpc=vpc)

        ecr_repo = cdk.aws_ecr.Repository(self, "NRL_ECR_REPO")

        task_definition = cdk.aws_ecs.FargateTaskDefinition(
            self, "NRL_TASK_DEF")

        container = task_definition.add_container(
            "NRL_CONTAINER",
            image=cdk.aws_ecs.ContainerImage.from_ecr_repository(ecr_repo),
            memory_limit_mib=512,
            logging=cdk.aws_ecs.LogDriver.aws_logs(
                stream_prefix="NRL_APP",
                log_retention=cdk.aws_logs.RetentionDays.ONE_WEEK,
            ),
        )

        for env in environment:
            container.add_environment(env, environment[env])
        container.add_port_mappings(cdk.aws_ecs.PortMapping(container_port=80))

        ecr_repo.grant_pull(task_definition.execution_role)

        # lb = cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer(
        #     self, "NRL_LB",
        #     vpc=vpc,
        #     internet_facing=True,  # Set to False if you want the load balancer to be internal
        #     load_balancer_name="NRLApplicationLoadBalancer"
        # )

        # for ip in allowed_ips:
        #     lb.connections.allow_from(
        #         cdk.aws_ec2.Peer.ipv4(ip.replace("\n", "")),
        #         cdk.aws_ec2.Port.tcp(lb_port)
        #     )

        # listener = lb.add_listener(
        #     "Listener",
        #     port=lb_port,
        #     open=True
        # )

        hosted_zone = cdk.aws_route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name=zone
        )

        certificate = cdk.aws_certificatemanager.Certificate(self, "NRLCertificate",
                                                             domain_name=domain,
                                                             validation=cdk.aws_certificatemanager.CertificateValidation.from_dns(
                                                                 hosted_zone)
                                                             )

        # listener.add_certificates("NRLCertificate", [certificate])

        # dns_record = cdk.aws_route53.CnameRecord(
        #     self, "NRLRecord",
        #     zone=hosted_zone,
        #     record_name=domain,
        #     domain_name=lb.load_balancer_dns_name
        # )

        fargate_service_sg = cdk.aws_ec2.SecurityGroup(
            self, "NRLServiceSG",
            vpc=vpc,
            allow_all_outbound=True
        )

        # lb.connections.allow_from(
        #     fargate_service_sg, cdk.aws_ec2.Port.tcp(ecs_port))

        fargate_service = cdk.aws_ecs.FargateService(
            self, "NRL_SERVICE",
            cluster=cluster,
            task_definition=task_definition,
            security_groups=[fargate_service_sg],
            assign_public_ip=True
        )

        # target_group = listener.add_targets(
        #     "ECS",
        #     port=ecs_port,
        #     targets=[fargate_service]
        # )


class DynamodbStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        f = open("../data/teams", "r")
        teams = f.read().splitlines()
        f.close()

        teams = {team.split(":")[0]: team.split(":")[1] for team in teams}

        for team in teams:
            team_id = teams[team]
            current_team = cdk.aws_dynamodb.Table(
                self, f"{team}Table",
                table_name=team,
                partition_key=cdk.aws_dynamodb.Attribute(
                    name="TeamName",
                    type=cdk.aws_dynamodb.AttributeType.STRING
                ),
                read_capacity=5,
                write_capacity=5
            )

        ladder = cdk.aws_dynamodb.Table(
            self, "LadderTable",
            table_name="Ladder",
            partition_key=cdk.aws_dynamodb.Attribute(
                name="TeamName",
                type=cdk.aws_dynamodb.AttributeType.STRING
            ),
            read_capacity=5,
            write_capacity=5
        )

        NRL2024Rounds = cdk.aws_dynamodb.Table(
            self, "NRL2024RoundsTable",
            table_name="NRL2024Rounds",
            partition_key=cdk.aws_dynamodb.Attribute(
                name="Round",
                type=cdk.aws_dynamodb.AttributeType.NUMBER
            ),
            read_capacity=5,
            write_capacity=5
        )
