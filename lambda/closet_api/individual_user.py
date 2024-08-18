import json
import boto3
from closet_api.users import check_user_exists

dynamodb = boto3.resource("dynamodb")

def get_user_information(event, table_name):
    username = event["pathParameters"]["username"]
    db_table = dynamodb.Table(table_name)
    db_response = db_table.get_item(Key={
        "username":username
    })
    user_object = db_response.get("Item")
    user_object.pop("password")
    return {
        "statusCode":200,
        "body":json.dumps(user_object)
    }

def delete_user(event, table_name, bucket):
    #Change to get from path
    user_to_delete = event["pathParameters"]["username"]

    db_table = dynamodb.Table(table_name)
    user_object = db_table.get_item(Key={
        "username":user_to_delete
    })
    user = user_object.get("Item", dict())
    uid = user.get("UserID")

    db_table.delete_item(Key={
        "username":user_to_delete
    })
    s3 = boto3.resource("s3")
    s3bucket = s3.Bucket(bucket)
    s3bucket.objects.filter(Prefix=f"{uid}/").delete()

    return {
        "statusCode":200,
        "body":json.dumps({"message":"User was successfully deleted"})
    }

def update_user(event, table_name):
    username = event["pathParameters"]["username"]
    new_username = event.get("queryStringParameters", dict()).get("new_username")
    
    if not check_user_exists(username, table_name):
        return {
            "statusCode":200,
            "body":json.dumps({"message":"This user does not exist"})
        }

    #Only if new_username is there
    if check_user_exists(new_username, table_name):
        return {
            "statusCode":200,
            "body":json.dumps({"message":"The username that you are requesting is already in use"})
        }
    
    table = dynamodb.Table(table_name)
    #Can't really work because this is a partition key
    table.update_item(Key={"username":username}, AttributeUpdates={"username":{"Value":new_username}})

    return {
        "statusCode":200,
        "body":json.dumps({"message":"We have successfully updated the username for this user"})
    }

def individual_user_handler(event, method, table_name, bucket):
    if method == "DELETE":
        return delete_user(event, table_name, bucket)
    if method == "PUT":
        update_user(event, table_name)
    if method == "GET":
        return get_user_information(event, table_name)
    else:
        return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unsupported method'})
            }