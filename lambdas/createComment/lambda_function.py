import json
import uuid
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    commentObject = json.loads(event['body'])
    key = str(uuid.uuid4())
    commentObject["id"] = key
    
    print(commentObject)
    
    dbResource =  boto3.resource('dynamodb')
    dbTable = dbResource.Table('comment')    
    
    dbTable.put_item(
    Item={
        "id":key,
         "value": json.dumps(commentObject)
    })
    
    return {
        'statusCode': 200,
        'body': json.dumps(commentObject)
    }
