import boto3
import requests
import pandas as pd
import numpy as np
import json
import ast
import random


df = pd.read_csv("user-events_new.csv")


s3urlClient =  boto3.client('s3',region_name = "us-east-1",aws_access_key_id="AKIA4LDBWFESAPUBTU7X",aws_secret_access_key= "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")

for index,row in df.iterrows():

    id = row["id"]

    url = 'https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_update/{id}'.format(id=id)
    
    tagURl = {'Online':['Online2.jpg','Online1.jpg'] , 'Morningside':['MorningSide1.jpg','MorningSide2.jpg'], 'Arts':['Arts1.jpg','Arts2.jpg'], 'Humanities':['Humanity1.jpg','Humanity2.jpg'], 'International and Public Affairs':['INTERNATIONALAFFAIRS1.png'], 'Graduate School of Arts and Sciences':['GSAS2.png','GSAS1.png'],'Seminar':['seminar2.jpg','seminar1.jpg'],'Social Sciences':["socialscience1.jpg",'socialscience2.png']}


    #print(row["attendees"])

    tag = list(row['tags'].split(";"))[0]


    data = {"imageUrl": s3urlClient.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': 'eventstaticcontent', 'Key': random.choice(tagURl[tag])} ,ExpiresIn=3600) }
    
  
    data_json = json.dumps({
        'doc': data
    })

    headers = {"Authorization":"Basic bWFzdGVyOlJhbmRvbSMxMjM=", "Content-Type":'application/json'}
    response = requests.post(url, data=data_json, headers=headers)

    if (index)%20 == 0:
        print("Processed Events:",index+1)