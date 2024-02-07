from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_logs as logs,
    aws_ecr as ecr,
    aws_dynamodb as dynamodb,
    aws_elasticloadbalancingv2 as elbv2,
    Stack
)
from constructs import Construct

file = open("../application_whitelist/whitelist.txt", "r")
allowed_ips = file.readlines()
file.close()


class FlaskFargateStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(self, "NRL_VPC", max_azs=2)

        cluster = ecs.Cluster(self, "NRL_CLUSTER", vpc=vpc)

        ecr_repo = ecr.Repository(self, "NRL_ECR_REPO")

        task_definition = ecs.FargateTaskDefinition(self, "NRL_TASK_DEF")

        container = task_definition.add_container(
            "NRL_CONTAINER",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repo),
            memory_limit_mib=512,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="NRL_APP",
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
        )

        container.add_environment("FLASK_ENV", "production")
        container.add_environment("FLASK_APP", "app.py")
        container.add_port_mappings(ecs.PortMapping(container_port=80))

        ecr_repo.grant_pull(task_definition.execution_role)

        lb = elbv2.ApplicationLoadBalancer(
            self, "NRL_LB",
            vpc=vpc,
            internet_facing=True,  # Set to False if you want the load balancer to be internal
            load_balancer_name="NRLApplicationLoadBalancer"
        )

        for ip in allowed_ips:
            lb.connections.allow_from(
                ec2.Peer.ipv4(ip.replace("\n", "")),
                ec2.Port.tcp(80)
            )

        listener = lb.add_listener(
            "Listener",
            port=80,
            open=True
        )

        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name="shadbury.com"
        )

        
        dnr_record = route53.ARecord(
            self, "NRLRecord",
            zone=hosted_zone,
            record_name="nrl.tracker.shadbury.com",
            target=route53.RecordTarget.from_alias(
                targets.LoadBalancerTarget(lb))
        )
        
        dns_record.node.add_dependency(lb)

        fargate_service_sg = ec2.SecurityGroup(
            self, "NRLServiceSG",
            vpc=vpc,
            allow_all_outbound=True
        )
        lb.connections.allow_from(fargate_service_sg, ec2.Port.tcp(80))

        fargate_service = ecs.FargateService(
            self, "NRL_SERVICE",
            cluster=cluster,
            task_definition=task_definition,
            security_groups=[fargate_service_sg],
            assign_public_ip=True
        )

        target_group = listener.add_targets(
            "ECS",
            port=80,
            targets=[fargate_service]
        )
        


class DynamodbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get Teams from file
        f = open("../data/teams", "r")
        teams = f.read().splitlines()
        f.close()

        # Create a dictionary of teams
        teams = {team.split(":")[0]: team.split(":")[1] for team in teams}

        # Create a table for each team
        for team in teams:
            team_id = teams[team]
            current_team = dynamodb.Table(
                self, f"{team}Table",
                table_name=team,
                partition_key=dynamodb.Attribute(
                    name="TeamName",
                    type=dynamodb.AttributeType.STRING
                ),
                read_capacity=5,
                write_capacity=5
            )

        # Ladder Table
        ladder = dynamodb.Table(
            self, "LadderTable",
            table_name="Ladder",
            partition_key=dynamodb.Attribute(
                name="TeamName",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=5,
            write_capacity=5
        )
