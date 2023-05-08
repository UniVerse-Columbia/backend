import json
import uuid
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    eventObject =  event["body-json"]
    
    key = str(uuid.uuid4())
    
    dbResource =  boto3.resource('dynamodb')
    dbTable = dbResource.Table('event')    
    
    eventObject["id"] = key
    
    dbTable.put_item(
    Item={
        "id":key,
         "value": json.dumps(eventObject)
    })
    
    return {
        'statusCode': 200,
        'body': json.dumps(eventObject)
    }
