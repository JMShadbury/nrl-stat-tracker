import os
import aws_cdk as cdk
from nrl_backend.nrl_backend import FlaskFargateStack, DynamodbStack

dynamodb_stack = cdk.App()
DynamodbStack(dynamodb_stack, "DynamodbStack",)

fargate_stack = cdk.App()
FlaskFargateStack(fargate_stack, "FargateStack",
    )
dynamodb_stack.synth()
fargate_stack.synth()
