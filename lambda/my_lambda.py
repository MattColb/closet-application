import boto3
import os
import json

dynamodb = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"] 

def handler(event, context):
    http_method = event["httpMethod"]
    if http_method == "GET":
        response = dynamodb.scan(TableName = table_name)
        return {
                'statusCode': 200,
                'body': json.dumps(response['Items'])
            }
    else:
        return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unsupported method'})
            }