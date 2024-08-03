import uuid
from datetime import datetime
import json

def create_user(event, table_name, bucket):
    body = event["body"]
    new_user = dict()
    new_user["creation_date"] = str(datetime.now())
    new_user["uid"] = uuid.uuid4()
    new_user["clothing_list"] = []
    new_user["username"] = body["username"]
    #Encrypt the password?
    new_user["password"] = body["password"]
    pass

def get_user_information():
    pass

def update_user():
    pass

def delete_user():
    pass

def user_handler(event, method, table_name, bucket):
    body = event["body"]
    if method == "GET":
        pass
    if method == "POST":
        pass
    if method == "DELETE":
        pass
    if method == "PUT":
        pass
    else:
        return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unsupported method'})
            }
    pass