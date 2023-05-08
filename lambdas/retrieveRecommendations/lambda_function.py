import json
import boto3

def lambda_handler(event, context):
    # Current implementation we are fetching all the events 
    # Later we need to modify it to use a user id based recommendation system
    
    print(event)
    
    userId = event['params']['path']['userId']
    
    dbResource =  boto3.resource('dynamodb')
    dbTable = dbResource.Table('event')    
    
    response = dbTable.scan()
    results = response['Items']
    
    retrieveUserArn = 'arn:aws:lambda:us-east-1:848460917028:function:retrieveUser'
    
    lambdaClient = boto3.client('lambda')

    
    recs = []
    for result in results:
        obj = {}
        print(result)
        
        result = json.loads(result['value'])
        
        obj["eventId"] = result["id"]
        obj["eventName"] = result["title"]
        obj["eventDescription"] = result["description"]
        obj["organizerId"] = result["organizerId"]
        obj["timestamp"] = result["timeStamp"]['timestamp']
        obj["location"] = result["location"]
        
        # fetching the name of organizer from the userpool using the getUser lambda
        
        data = {'params':{'path':{'userId':obj["organizerId"]}}}

        response = lambdaClient.invoke(FunctionName=retrieveUserArn,
                                 InvocationType='RequestResponse',
                                 Payload=json.dumps(data))
        
        organizerResp = json.loads(response.get('Payload').read())
        print(organizerResp)
        
        organizerBody = json.loads(organizerResp['body'])
        
        obj["organizerName"] = organizerBody["firstName"] + " " + organizerBody["lastName"] 
        
        recs.append(obj)
        
    return {
        'statusCode': 200,
        'body': {"eventIds":json.dumps(recs)}
    }
