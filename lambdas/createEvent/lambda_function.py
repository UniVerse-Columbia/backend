import json
import uuid
import requests
import boto3
import random
#import create_message

def add_data_to_opensearch(itemKey, data):
    DOMAIN_ENDPOINT = "https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_doc/"
   
    headers = {"Authorization":"Basic bWFzdGVyOlJhbmRvbSMxMjM=", "Content-Type":'application/json'}
   
    resp = requests.put(DOMAIN_ENDPOINT+itemKey, data=json.dumps(data), headers=headers)
    
    print(resp)
    if resp.status_code == 201 or resp.status_code == 200:
        
        publish_message_sns(data)
        
        return {"statusCode":200,
                "body":data}
    else:
        return {"statusCode":500,
                "body":resp.content}
        
    
def lambda_handler(event, context):
    # TODO implement
    eventObject =  event["body-json"]
    
    key = str(uuid.uuid4())
    eventObject["id"] = key

    s3urlClient =  boto3.client('s3',region_name = "us-east-1",aws_access_key_id="AKIA4LDBWFESAPUBTU7X",aws_secret_access_key= "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")

    tagURl = {'Online':['Online2.jpg','Online1.jpg'] , 'Morningside':['MorningSide1.jpg','MorningSide2.jpg'], 'Arts':['Arts1.jpg','Arts2.jpg'],
    'Humanities':['Humanity1.jpg','Humanity2.jpg'], 'International and Public Affairs':['INTERNATIONALAFFAIRS1.png'], 
    'Graduate School of Arts and Sciences':['GSAS2.png','GSAS1.png'],'Seminar':['seminar2.jpg','seminar1.jpg'],
    'Social Sciences':["socialscience1.jpg",'socialscience2.png']}

    #print(row["attendees"])

    tag = eventObject["tags"][0]["tagName"]

    eventObject["imageUrl"] = s3urlClient.generate_presigned_url(ClientMethod='get_object', 
    Params={'Bucket': 'eventstaticcontent', 'Key': random.choice(tagURl[tag])} ,ExpiresIn=172800) 

    print(eventObject)
    
    return add_data_to_opensearch(key, eventObject)

def publish_message_sns(body):
    
    eventTags = ""
    
    tagList = body['tags']
    
    snsClient = boto3.client('sns')
    
    baseTopicArn = "arn:aws:sns:us-east-1:848460917028:"
    
    for tag in tagList:
        
        # Publishing Message to Topic
        
        topicArn = baseTopicArn + tag["tagName"].replace(" ","_") 
        
        message = "New event:"+body["title"]+" with tag:"+tag["tagName"] + " created."
        
        resp = snsClient.publish(TopicArn=topicArn, Message=message)
        print(resp)
    