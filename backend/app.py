import os
import aws_cdk as cdk
from nrl_backend.nrl_backend import FlaskFargateStack, DynamodbStack

dynamodb_stack = cdk.App()
DynamodbStack(dynamodb_stack, "DynamodbStack",)

app = cdk.App()
FlaskFargateStack(app, "FargateStack",
    )

app.synth()
dynamodb_stack.synth()