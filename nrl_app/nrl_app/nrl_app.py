from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_logs as logs,
    aws_ecr as ecr,
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

        ecr_repo.grant_pull(task_definition.execution_role)

        task_role = iam.Role(self, "NRL_TASK_ROLE", assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"))
        
        print(vpc.vpc_default_security_group)

        ecs.FargateService(
            self, "NRL_SERVICE",
            cluster=cluster,
            task_definition=task_definition,
            assign_public_ip=True
        )
