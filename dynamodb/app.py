#!/usr/bin/env python3
import os

import aws_cdk as cdk

from dynamodb.dynamodb_stack import DynamodbStack


dynamodb_stack = cdk.App()
DynamodbStack(app, "DynamodbStack",)

dynamodb_stack.synth()
