from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_logs as logs,
    aws_ecr as ecr,
    aws_elasticloadbalancingv2 as elbv2,
    Stack
)
from constructs import Construct

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

        task_role = iam.Role(self, "NRL_TASK_ROLE", assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"))
    
        
        lb = elbv2.ApplicationLoadBalancer(
            self, "NRL_LB",
            vpc=vpc,
            internet_facing=True,  # Set to False if you want the load balancer to be internal
            load_balancer_name="NRLApplicationLoadBalancer"
        )
        
        lb.connections.allow_from(
            ec2.Peer.ipv4("101.188.67.134/32"),
            ec2.Port.tcp(80)
        )
        
        
        listener = lb.add_listener(
            "Listener",
            port=80,
            open=True
        )
        
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