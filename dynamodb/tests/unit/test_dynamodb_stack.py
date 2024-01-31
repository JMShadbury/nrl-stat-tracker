import aws_cdk as core
import aws_cdk.assertions as assertions

from dynamodb.dynamodb_stack import DynamodbStack

# example tests. To run these tests, uncomment this file along with the example
# resource in dynamodb/dynamodb_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DynamodbStack(app, "dynamodb")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
