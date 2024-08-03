from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    # aws_sqs as sqs,
)
from constructs import Construct

#Find someway to login

class ClosetApplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #User Resource
        #Clothing Resource (Create, Update, Delete, Get)
        #Photos?

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
        bucket = s3.Bucket(self, "ClosetApplication")

        table = dynamodb.Table(self, 'API_dynamodb',
                               partition_key=dynamodb.Attribute(name="UserID", type=dynamodb.AttributeType.STRING),
                               table_name="API_dynamodb_test")

        #S3 to store photos of clothes

        #Lambda(s) to get and process the data
        user_lambda = _lambda.Function(self, 'API_Handler',
                                           runtime=_lambda.Runtime.PYTHON_3_11,
                                            code = _lambda.Code.from_asset('lambda'),
                                            handler = "user_lambda.handler",
                                            environment={
                                                "TABLE_NAME":table.table_name,
                                                "BUCKET_NAME":bucket.bucket_name
                                            } )
        
        clothing_lambda = _lambda.Function(self, 'API_Handler',
                                           runtime=_lambda.Runtime.PYTHON_3_11,
                                            code = _lambda.Code.from_asset('lambda'),
                                            handler = "clothing_lambda.handler",
                                            environment={
                                                "TABLE_NAME":table.table_name,
                                                "BUCKET_NAME":bucket.bucket_name
                                            } )
        
        table.grant_full_access(user_lambda)
        bucket.grant_read_write(user_lambda)

        table.grant_full_access(clothing_lambda)
        bucket.grant_read_write(clothing_lambda)

        #API Gateway to hit Lambda Functions
        api = apigateway.RestApi(self, "MyAPI",
                                 rest_api_name="closet_application",
                                 description="test api for the closet app")
        
        user_integration = apigateway.LambdaIntegration(user_lambda,
                                                       request_templates={'application/json': '{"statusCode": "200"}'})

        items = api.root.add_resource("users")
        items.add_method("GET", user_integration)
        items.add_method("POST", user_integration)
        items.add_method("DELETE", user_integration)
        items.add_method("PUT", user_integration)

        clothing_integration = apigateway.LambdaIntegration(clothing_lambda,
                                                       request_templates={'application/json': '{"statusCode": "200"}'})

        items = api.root.add_resource("users")
        items.add_method("GET", clothing_integration)
        items.add_method("POST", clothing_integration)
        items.add_method("DELETE", clothing_integration)
        items.add_method("PUT", clothing_integration)

        #S3 to host the website files. They make calls to the API gateway API to get the data that is needed