import json
import boto3
from datetime import datetime
import logging
from string import Template
import requests
import random

def get_data_from_opensearch(id):
    url = 'https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_doc/{id}'.format(id=id)
    headers = {"Authorization":"Basic bWFzdGVyOlJhbmRvbSMxMjM=", "Content-Type":'application/json'}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        eventObject = json.loads(response.content)['_source']
        return eventObject
    else:
        return {"statusCode":500,
                "body":response.content}

def get_matched_popularity_recs(userId, tags, defaultSize, event):
    # Make a OpenSearch search query to fetch events with these usernames
    
    DOMAIN_ENDPOINT = 'https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_search'
    headers = {"Authorization":"Basic bWFzdGVyOlJhbmRvbSMxMjM=", "Content-Type":'application/json'}
    
    query = {"bool":{"should":[]}}
    
    shouldQuery= []
    
    for tag in tags:
        shouldQuery.append({"match":{"tags.tagName":tag}})
    
    query["bool"]["should"] = shouldQuery
    requestBody = {"size":2*defaultSize,"query":query }
    
    
    resp = requests.post(DOMAIN_ENDPOINT,data=json.dumps(requestBody),headers=headers)
    
    content = json.loads((resp.content.decode('utf-8')))
    
    eventResults = content["hits"]["hits"]
    
    eventResults.sort(key= lambda x: len(x["_source"]["attendee"]), reverse = True)
    
    resultArr = []
    
    for event in eventResults:
        if userId not in event["_source"]["attendee"]:
            resultArr.append(event["_source"]) 
            
    return resultArr

def get_personalize_recs(userId, tags, defaultSize, event):
    personalizeRt = boto3.client('personalize-runtime')
    try:
        response = personalizeRt.get_recommendations(
            campaignArn = 'arn:aws:personalize:us-east-1:848460917028:campaign/personalizer',
            userId = userId,
            numResults = 2*defaultSize
        )
        
        events = []
        for item in response['itemList']:
            event = get_data_from_opensearch(item['itemId'])
        
            # first filter - the user should not have already attended the event
            if userId not in event['attendee']:
                common_tags = set(event['tags']).intersection(set(tags))
                
                # second filter - the event should have atleast one common tag with the user's preferred tags
                if len(common_tags) >=1:
                    events.append(event)
            
        return events
        
    except Exception as e:
        print(e)
        return []

def lambda_handler(event, context):
    print(event)
    userId = event['params']['path']['userId'].strip()
    
    try:
        cognitoClient = boto3.client("cognito-idp")
    
        user = cognitoClient.admin_get_user(
            UserPoolId='us-east-1_C8J5HLL6q',
            Username=userId
        )
        
        tags = list(filter( lambda x: x['Name'] == 'custom:tags', user["UserAttributes"]))[0]
        
        tags = list(tags['Value'].split(";"))
        
        defaultSize = 20
        if "querystring" in event["params"] and "size" in event['params']['querystring']:
            defaultSize = int(event['params']['querystring']['size'])
    
        print("Default Size:", defaultSize)
        
        personalized_events = get_personalize_recs(userId, tags, defaultSize, event)
        popularity_events = get_matched_popularity_recs(userId, tags, defaultSize, event)
        
        
        # personalized events take precedence, after which any additional popularity based events are added to the final list
        for event in popularity_events:
            if event not in personalized_events:
                personalized_events.append(event)
    
        return {
            "statusCode": 200,
            "body": personalized_events
        }
        
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": []
        }
