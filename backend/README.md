
# FlaskFargateStack and DynamodbStack README

## Overview
This README provides documentation for the `FlaskFargateStack` and `DynamodbStack` classes. These classes are part of a Python application that uses the AWS Cloud Development Kit (AWS CDK) to define cloud infrastructure in code and provision it through AWS CloudFormation. The application is designed to deploy a Flask-based application on AWS Fargate with an Application Load Balancer and to create DynamoDB tables for team data management.

## Requirements
- AWS CDK
- Python 3.x
- An AWS account and AWS CLI configured with appropriate credentials.

## FlaskFargateStack

### Description
The `FlaskFargateStack` class defines a stack for deploying a containerized Flask application using AWS Fargate. It includes the following resources:
- A VPC with a maximum of two Availability Zones.
- An ECS cluster.
- An ECR repository for the container image.
- A Fargate task definition with a single container.
- An Application Load Balancer (ALB) with security settings that allow traffic from specific IP addresses.
- Necessary IAM roles and security groups.

### Features
- **ECS Fargate Deployment**: Automatically deploys a Flask application in a serverless environment.
- **Load Balancer**: Uses an Application Load Balancer to distribute incoming application traffic.
- **Security**: Restricts access to the load balancer based on a list of allowed IP addresses.
- **Logging**: Configures AWS Logs for the container, retaining logs for one week.

### How to Deploy
1. Ensure your AWS credentials are set up.
2. Run `cdk deploy` to deploy the stack defined in this class.

## DynamodbStack

### Description
The `DynamodbStack` class defines a stack for creating DynamoDB tables. It reads team data from a file and creates a DynamoDB table for each team, as well as a 'Ladder' table.

### Features
- **Team Tables Creation**: Creates individual DynamoDB tables for each team listed in the `../data/teams` file.
- **Ladder Table**: Creates a separate DynamoDB table named 'Ladder' for additional data management.

### How to Deploy
1. Ensure your AWS credentials are set up.
2. Run `cdk deploy` to deploy the stack defined in this class.

## Security Considerations
- Ensure that the list of allowed IPs for the ALB in `FlaskFargateStack` is managed and updated securely.
- Review IAM roles and policies for least privilege access.

## Additional Notes
- Modify the application and team data as needed before deployment.
- Monitor AWS resources for cost management.

---

For further customization or troubleshooting, refer to the AWS CDK documentation and AWS best practices.
