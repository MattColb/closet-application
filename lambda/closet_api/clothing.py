from datetime import datetime
import uuid

#                    {ClothingDescription:
        #             PrimaryColor:
        #             ClothingType:
        #             ClothingID:
        #             PurchaseDate:
        #             Tags: []
        #             WearDates: [01-12-22]
        #         }

def add_wear(clothing_id, date=None):
    if date == None:
        str(datetime.now())
    pass

def add_piece_of_clothing(event, table_name, bucket_name):
    body = json.loads(event["body"])
    clothing = dict()
    clothing["ClothingID"] = str(uuid.uuid4())
    clothing["Tag"] = []
    clothing["WearDates"] = []
    clothing["PurchaseDate"] = ""
    clothing["PrimaryColor"] = ""
    clothing["ClothingDescription"] = ""
    clothing["ClothingType"] = "" #Take this from a set?
s    pass

def clothes_handler(event, method, table_name, bucket_name):
    if method == "GET":
        pass
    if method == "POST":
        pass
    if method == "PUT":
        pass
    if method == "DELETE":
        pass

    pass