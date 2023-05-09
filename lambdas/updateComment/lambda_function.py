import json
import uuid
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    
    id = event['pathParameters']['commentId']
    commentObject = json.loads(event['body'])
    
    dbResource =  boto3.resource('dynamodb')
    dbTable = dbResource.Table('comment')    
    
    print(json.dumps(commentObject))
    
    response = dbTable.put_item(
    Item={
        "id" : id,
        "value" : json.dumps(commentObject)
    })
    
    print("RESPONSE FROM dbTABLE: ",response)
    
    return {
        'statusCode': 200,
        'body': json.dumps(commentObject)
    }

