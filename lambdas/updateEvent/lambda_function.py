import json
import uuid
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    
    id = event['params']['path']['eventId']
    eventObject = event['body-json']
    
    dbResource =  boto3.resource('dynamodb')
    dbTable = dbResource.Table('event')    
    
    print(json.dumps(eventObject))
    
    response = dbTable.put_item(
    Item={
        "id" : id,
        "value" : json.dumps(eventObject)
    })
    
    print("RESPONSE FROM dbTABLE: ",response)
    
    return {
        'statusCode': 200,
        'body': json.dumps(eventObject)
    }

