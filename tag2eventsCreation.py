import boto3
import pandas as pd
import numpy as np

dbclient =  boto3.resource('dynamodb',region_name = "us-east-1",aws_access_key_id="AKIA4LDBWFESAPUBTU7X",aws_secret_access_key= "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")
table = dbclient.Table('tag2events')
tag2event = {}

df = pd.read_csv("shortlisted_events.csv")

for index,row in df.iterrows():

    tagValues =  "".join(row["tags"])

    for tag in tagValues.split(";"):
        
        if tag not in tag2event:
            tag2event[tag] = []
        
        tag2event[tag].append(row["id"])
    
for key in tag2event:
    table.put_item(Item={  "tag":key,"events": tag2event[key]})

