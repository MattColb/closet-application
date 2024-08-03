import boto3
import os
import json
import closet_api.profile as user_profile

dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
bucket_name = os.environ["BUCKET_NAME"]
table_name = os.environ["TABLE_NAME"] 

def handler(event, context):
    
    method = event["httpMethod"]
    api_path = event["path"]
    
    if api_path == "/user":
        return user_profile.user_handler(event, method, table_name, bucket_name)
    else:
        return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unsupported method'})
            }