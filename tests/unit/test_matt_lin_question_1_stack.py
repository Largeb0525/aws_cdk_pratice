import aws_cdk as core
import aws_cdk.assertions as assertions

from matt_lin_question_1.matt_lin_question_1_stack import MattLinQuestion1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in matt_lin_question_1/matt_lin_question_1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MattLinQuestion1Stack(app, "matt-lin-question-1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
