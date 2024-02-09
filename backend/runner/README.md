# NIB GitLab Runner

## Description

This module will create the following resources.

AWS::EC2::SecurityGroup
AWS::IAM::Role
AWS::IAM::InstanceProfile
AWS::AutoScaling::AutoScalingGroup
AWS::SSM::Parameter

Once the resources are created, the userdatatemplate will install required resources and register the runner with CMD's gitlab.


## Deployment Example

## install requirements

```npm install```

### bootstrap

```cdk bootstrap --profile <aws profile>```

### deploy

```CLIENT="aonsw" cdk deploy --profile <aws profile>```


