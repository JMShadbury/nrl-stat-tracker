import aws_cdk as core
import aws_cdk.assertions as assertions

from nrl_front_end.nrl_front_end_stack import NrlFrontEndStack

# example tests. To run these tests, uncomment this file along with the example
# resource in nrl_front_end/nrl_front_end_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = NrlFrontEndStack(app, "nrl-front-end")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
