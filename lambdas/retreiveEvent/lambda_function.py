import json
import uuid
import requests

def get_data_from_opensearch(id):
    url = 'https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_doc/{id}'.format(id=id)
    headers = {"Authorization":"Basic bWFzdGVyOlJhbmRvbSMxMjM=", "Content-Type":'application/json'}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        eventObject = json.loads(response.content)['_source']
        return {"statusCode":200,
                "body":eventObject}
    else:
        return {"statusCode":500,
                "body":response.content}

def lambda_handler(event, context):
    # TODO implement
    
    print(event)
    id = event['params']['path']['eventId']
    
    return get_data_from_opensearch(id)