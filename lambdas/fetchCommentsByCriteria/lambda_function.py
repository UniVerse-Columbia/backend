import json
import uuid
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    
    criteria_list = json.loads(event['body'])
    
    eventId = criteria_list[0]['values']
    
    print(eventId)
    print(type(eventId))
    
    dbResource =  boto3.resource('dynamodb')
    dbTable = dbResource.Table('comment') 
    
    response = dbTable.scan(
        FilterExpression=Attr('value').contains(eventId)
    )
    comments_unparsed = response['Items']
    comments = []
    for comment_unparsed in comments_unparsed:
        comments.append(json.loads(comment_unparsed['value']))
        
    return {
        'statusCode': 200,
        'body': json.dumps(comments)
    }
