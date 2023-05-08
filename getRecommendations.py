import boto3
import requests
import json

userId = 'alexis_newman'

cognitoClient = boto3.client("cognito-idp",region_name = "us-east-1",aws_access_key_id="AKIA4LDBWFESAPUBTU7X",aws_secret_access_key= "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")

user = cognitoClient.admin_get_user(
    UserPoolId='us-east-1_C8J5HLL6q',
    Username=userId
)

tags = list(filter( lambda x: x['Name'] == 'custom:tags', user["UserAttributes"]))[0]

tags = list(tags['Value'].split(";"))

# Make a OpenSearch search query  to fetch events with these usernames

DOMAIN_ENDPOINT = 'https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_search'
headers = {"Authorization":"Basic bWFzdGVyOlJhbmRvbSMxMjM=", "Content-Type":'application/json'}

query = {"bool":{"should":[]}}

shouldQuery= []

for tag in tags:
    shouldQuery.append({"match":{"tags.tagName":tag}})

query["bool"]["should"] = shouldQuery
requestBody = {"size":2,"query":query }


resp = requests.post(DOMAIN_ENDPOINT,data=json.dumps(requestBody),headers=headers)

content = json.loads((resp.content.decode('utf-8')))

eventResults = content["hits"]["hits"]

eventResults.sort(key= lambda x: len(x["_source"]["attendee"]), reverse = True)

resultArr = []

for event in eventResults:
    if userId not in event["_source"]["attendee"]:
        resultArr.append(event["_source"]) 

print(len(resultArr))




