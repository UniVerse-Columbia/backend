import json
import uuid
import requests

def delete_data_from_opensearch(id):
    url = 'https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_doc/{id}'.format(id=id)
    headers = {"Authorization":"Basic bWFzdGVyOlJhbmRvbSMxMjM=", "Content-Type":'application/json'}
    
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return {"statusCode":200,
                "body":"Event with id:{id} is deleted".format(id=id)}
    else:
        return {"statusCode":500,
                "body":response.content}

def lambda_handler(event, context):
    # TODO implement
    
    print(event)
    id = event['params']['path']['eventId']
    
    return delete_data_from_opensearch(id)