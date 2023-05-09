import json
import uuid
import requests

def get_data_from_opensearch(criteria_list):
    DOMAIN_ENDPOINT = 'https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_search'
    headers = {"Authorization":"Basic bWFzdGVyOlJhbmRvbSMxMjM=", "Content-Type":'application/json'}
    
    userId = None
    tags = []
    searchText = ""
    for criteria_object in criteria_list:
        if criteria_object['criteria'] == 'searchtext':
            searchText = criteria_object['values']
        
        elif criteria_object['criteria'] == 'tags':
            tags = criteria_object['values'].split(';')
    
        elif criteria_object['criteria'] == 'userId':
            userId = criteria_object['values']
    
    if userId:
        print('User ID: ', userId)
        query = {
            "terms": {
              "attendee": [userId]
            }
          }
    else:
        print("Search Text:", searchText)
        print("Tags:", tags)
        
        tagsShouldQuery= []
        for tag in tags:
            tagsShouldQuery.append({"match":{"tags.tagName":tag}})
        
        textShouldQuery = []
        textShouldQuery.append({"match": {"title": searchText}})
        textShouldQuery.append({"match": {"description": searchText}})
        
        print(tagsShouldQuery)
        print(len(searchText))
        
        if len(tags)==1 and tags[0]=='' and len(searchText)==0:
            print('Here')
            match_all = {}
            query = {
                        "match_all" : match_all
                    }
        elif len(tags)==1 and tags[0]=='':
            query = {
                        "bool": {
                            "should": textShouldQuery
                        }
                    }
        elif len(searchText)==0:
            query = {
                        "bool": {
                            "should": tagsShouldQuery
                        }
                    }
        else:
            query = {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": tagsShouldQuery
                            }
                        },
                        {
                            "bool": {
                                "should": textShouldQuery
                            }
                        }
                    ]
                }
            }

    requestBody = {"size":100,"query":query }
    response = requests.post(DOMAIN_ENDPOINT,data=json.dumps(requestBody),headers=headers)
    
    if response.status_code == 200:
        content = json.loads((response.content.decode('utf-8')))
        eventResults = content["hits"]["hits"]
        
        resultArr = []
        for event in eventResults:
            resultArr.append(event["_source"]) 
            
        print(resultArr)

        return {"statusCode":200,
                "body":json.dumps(resultArr)}
    else:
        return {"statusCode":500,
                "body":json.dumps(response.content)}

def lambda_handler(event, context):
    # TODO implement
    
    print(event)
    
    criteria_list = json.loads(event['body'])
    return get_data_from_opensearch(criteria_list)