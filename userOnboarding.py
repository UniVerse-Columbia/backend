import pandas as pd
import numpy as np
import boto3

df = pd.read_csv("organizer.csv")

client =  boto3.client('cognito-idp', region_name = "us-east-1",aws_access_key_id="AKIA4LDBWFESAPUBTU7X",aws_secret_access_key= "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")

for index, row in df.iterrows():
        UserAttributes=[{"Name":"given_name" ,"Value": row["given_name"]},{"Name":"family_name","Value": row["family_name"] if not pd.isnull(row["family_name"]) else ""}, {"Name":"email","Value":row["contactemail"]},{"Name":"phone_number","Value":row["contactphone"]},{"Name":"custom:tags","Value":row["custom:tags"]},{"Name":"custom:userType","Value":"organizer"},{ "Name": "email_verified", "Value": "true" }]
        print(UserAttributes)
        try:
            response = client.admin_create_user(UserPoolId="us-east-1_C8J5HLL6q",Username=row["cognito:username"],UserAttributes=UserAttributes,TemporaryPassword="Admin@12")
        except:
            continue
        if ((index+1)%20==0):
            print("Processed:",index+1,"entries")


DOMAIN_ENDPOINT = 'https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/events/_search'