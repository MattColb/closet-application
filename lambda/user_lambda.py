import boto3
import os
import json
import closet_api.users as user_profile
import closet_api.individual_user as individual_user

dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
bucket_name = os.environ["BUCKET_NAME"]
table_name = os.environ["TABLE_NAME"] 

def handler(event, context):
    
    method = event["httpMethod"]
    api_path = event["resource"]
    
    if api_path == "/users":
        return user_profile.user_handler(event, method, table_name, bucket_name)
    if api_path == "/users/{username}":
        return individual_user.individual_user_handler(event, method, table_name, bucket_name)
    else:
        return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unsupported path'})
            }