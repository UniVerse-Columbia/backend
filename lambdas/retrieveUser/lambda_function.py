import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    userId = event['pathParameters']['userId']
    
    print(userId)
    
    cognitoClient = boto3.client('cognito-idp')
    
    try:
        cognitoResponse = cognitoClient.admin_get_user(
                                                        UserPoolId='us-east-1_C8J5HLL6q',
                                                        Username=userId
                                                    )
        print(cognitoResponse)
        userObject = {}
        
        for attr in cognitoResponse['UserAttributes']:
            if attr["Name"] == 'given_name':
                userObject["given_name"] = attr["Value"]
            
            elif attr["Name"] == 'family_name':
                userObject["family_name"] = attr["Value"]
            
            elif attr["Name"] == "custom:tags":
                userObject["custom:tags"] = attr['Value']
                
            elif attr["Name"] == "custom:userType":
                userObject["custom:userType"] = attr['Value']
            
            elif attr["Name"] == "email":
                userObject["email"] = attr['Value']
            
            elif attr["Name"] == "phone_number":
                userObject["phone_number"] = attr['Value']
            
        
        return {
            'statusCode': 200,
            'body': json.dumps(userObject)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode' : 500,
            'body' : json.dumps({})
        }
