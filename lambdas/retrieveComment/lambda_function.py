import json
import uuid
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    dbClient =  boto3.client('dynamodb') 
    
    print(event)
    
    id = event['pathParameters']['commentId']
    
    event_response = dbClient.get_item(
    TableName='comment',
    Key={
        'id' : {'S' : id}
    }
    )
    
    print(event_response)
    
    comment_obj_str = event_response['Item']['value']['S']
    comment = json.loads(comment_obj_str)
    
    print(comment)
    
    return {
        'statusCode': 200,
        'body': json.dumps(comment)
    }