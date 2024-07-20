from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb
    # aws_sqs as sqs,
)
from constructs import Construct

class ClosetApplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Dynamo Table to keep track of users and clothes
        # {
        #     userID:
        #     Username:
        #     Password:
        #     CreationDate:
        #     ClothingList: [
        #         {
        #             ClothingDescription:
        #             PrimaryColor:
        #             ClothingType:
        #             ClothingID:
        #             PurchaseDate:
        #             WearDates: [01-12-22]
        #         }
        #     ]
        # }
        table = dynamodb.Table(self, 'API_dynamodb',
                               partition_key=dynamodb.Attribute(name="UserID", type=dynamodb.AttributeType.STRING),
                               table_name="API_dynamodb_test")

        #S3 to store photos of clothes

        #Lambda(s) to get and process the data
        lambda_function = _lambda.Function(self, 'API_Handler',
                                           runtime=_lambda.Runtime.PYTHON_3_11,
                                            code = _lambda.Code.from_asset('lambda'),
                                            handler = "my_lambda.handler",
                                            environment={
                                                "TABLE_NAME":table.table_name
                                            } )
        
        table.grant_full_access(lambda_function)

        #API Gateway to hit Lambda Functions
        api = apigateway.RestApi(self, "MyAPI",
                                 rest_api_name="closet_application",
                                 description="test api for the closet app")
        
        get_integration = apigateway.LambdaIntegration(lambda_function,
                                                       request_templates={'application/json': '{"statusCode": "200"}'})
        
        api.root.add_method("GET", get_integration)

        items = api.root.add_resource("items")
        items.add_method("GET", get_integration)

        #S3 to host the website files. They make calls to the API gateway API to get the data that is needed