import json
import uuid
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    dbClient =  boto3.client('dynamodb') 
    
    print(event)
    
    id = event['params']['path']['eventId']
    
    event_response = dbClient.get_item(
    TableName='event',
    Key={
        'id' : {'S' : id}
    }
    )
    
    print(event_response)
    
    event_obj_str = event_response['Item']['value']['S']
    event = json.loads(event_obj_str)
    
    print(event)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Got Event with event id:' + event['id'])
    }