import json
import uuid
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    dbClient =  boto3.client('dynamodb') 
    
    id = event['pathParameters']['eventid']
    
    dbClient.delete_item(
    TableName='event',
    Key={
        'id' : {'S' : id}
    }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Deleted Event with event id: ' + id)
    }
    
    
