import json
import uuid
import requests

def update_data_in_opensearch(data, id):
    url = 'https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_update/{id}'.format(id=id)
    data_json = json.dumps({
        'doc': data
    })
    headers = {"Authorization":"Basic bWFzdGVyOlJhbmRvbSMxMjM=", "Content-Type":'application/json'}
    response = requests.post(url, data=data_json, headers=headers)
    
    if response.status_code == 200:
        return {"statusCode":200,
                "body":data}
    else:
        return {"statusCode":500,
                "body":response.content}


def lambda_handler(event, context):
    # TODO implement
    print(event)
    
    id = event['params']['path']['eventId']
    eventObject = event['body-json']
    
    print(eventObject)
    
    return update_data_in_opensearch(eventObject, id)

