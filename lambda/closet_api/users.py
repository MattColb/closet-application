import uuid
from datetime import datetime
import json
import boto3

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

def check_user_exists(username, table_name):
    table = dynamodb.Table(table_name)
    db_response = table.get_item(Key={
        "username":username
    })
    user_object = db_response.get("Item")
    if user_object == None:
        return False
    else:
        return True
    

def create_user(event, table_name, bucket):
    body = json.loads(event["body"])

    if check_user_exists(body["username"], table_name):
        return {
            "statusCode":200,
            "body":json.dumps({"message":"That usename is already taken"})
        }


    new_user = dict()
    new_user["creation_date"] = str(datetime.now())
    new_user["UserID"] = str(uuid.uuid4())
    new_user["clothing_list"] = []
    new_user["username"] = body["username"]
    #Encrypt the password?
    new_user["password"] = body["password"]

    table = dynamodb.Table(table_name)
    table.put_item(Item=new_user)

    s3.put_object(Bucket=bucket, Key=new_user["UserID"]+"/")
    return {
        "statusCode":200,
        "body":json.dumps({"message":"User was successfully created"})
    }

def get_users(table_name):
    table = dynamodb.Table(table_name)
    all_information = table.scan(Select="SPECIFIC_ATTRIBUTES", ProjectionExpression="UserID,username,clothing_list,creation_date").get("Items")
    return {
        "statusCode":200,
        "body":json.dumps(all_information)
    }

def user_handler(event, method, table_name, bucket):
    if method == "GET":
        return get_users(table_name)
    if method == "POST":
        return create_user(event, table_name, bucket)
    else:
        return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unsupported method'})
            }
    pass