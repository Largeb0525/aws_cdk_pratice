from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_sqs as sqs,
)
from constructs import Construct
import json


class MattLinQuestion1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "TomofunMessageQueue",
        )

        lambda_function = _lambda.Function(
            self, "TomofunMessageHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_handler.main",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "QUEUE_URL": queue.queue_url
            }
        )
        queue.grant_send_messages(lambda_function)
        queue.grant_consume_messages(lambda_function)

        api = apigateway.RestApi(self, "TomofunMessageApi",rest_api_name="Tomofun Message Service")

        post_integration = apigateway.LambdaIntegration(lambda_function)
        api.root.add_method("POST", post_integration)

        get_integration = apigateway.LambdaIntegration(lambda_function)
        api.root.add_method("GET", get_integration)