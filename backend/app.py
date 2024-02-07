import os
import aws_cdk as cdk
from nrl_backend.nrl_backend import FlaskFargateStack, DynamodbStack

app = cdk.App()
DynamodbStack(app, "DynamodbStack",)

fargate_stack = cdk.App()
FlaskFargateStack(app, "FargateStack",
                  env={ 
                      'region': 'ap-southeast-2'
  }
    )
app.synth()
