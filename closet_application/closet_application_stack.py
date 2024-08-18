from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    RemovalPolicy
    # aws_sqs as sqs,
)
from constructs import Construct

#Find someway to login

class ClosetApplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "ClosetApplication", removal_policy=RemovalPolicy.DESTROY, auto_delete_objects=True)

        table = dynamodb.Table(self, 'API_dynamodb',
                               partition_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING),
                               table_name="API_dynamodb_test",
                               removal_policy=RemovalPolicy.DESTROY)

        #Lambda(s) to get and process the data
        user_lambda = _lambda.Function(self, 'user_api_handler',
                                           runtime=_lambda.Runtime.PYTHON_3_11,
                                            code = _lambda.Code.from_asset('lambda'),
                                            handler = "user_lambda.handler",
                                            environment={
                                                "TABLE_NAME":table.table_name,
                                                "BUCKET_NAME":bucket.bucket_name
                                            } )
        
        clothing_lambda = _lambda.Function(self, 'clothing_api_handler',
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


        #Just users should have post, and get all users? (login?)
        users = api.root.add_resource("users")
        users.add_method("GET", user_integration)
        users.add_method("POST", user_integration)

        individual_users = users.add_resource("{username}")

        #Users/{username} should have get (get user information), put to update username or password, delete to delete user
        individual_users.add_method("DELETE", user_integration)
        individual_users.add_method("PUT", user_integration)
        individual_users.add_method("GET", user_integration)

        clothing_integration = apigateway.LambdaIntegration(clothing_lambda,
                                                       request_templates={'application/json': '{"statusCode": "200"}'})

        #users/{username}/clothing should have get to get all clothes, and post to add an item
        items = api.root.add_resource("items")
        items.add_method("GET", clothing_integration)
        items.add_method("POST", clothing_integration)

        #users/{username}/clothing/{clothing-id} should have get to get specific information about the clothing,
        #Put to update tags, wears, closets and delete to delete the item
        items.add_method("DELETE", clothing_integration)
        items.add_method("PUT", clothing_integration)

        #S3 to host the website files. They make calls to the API gateway API to get the data that is needed