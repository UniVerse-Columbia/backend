import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    userId = event['params']['path']['userId']
    
    print(userId)
    
    cognitoClient = boto3.client('cognito-idp')
    
    cognitoResponse = cognitoClient.admin_get_user(
                                                    UserPoolId='us-east-1_C8J5HLL6q',
                                                    Username=userId
                                                )
    print(cognitoResponse)
    for attr in cognitoResponse['UserAttributes']:
        if attr["Name"] == 'given_name':
            fname = attr["Value"]
        if attr["Name"] == 'family_name':
            lname = attr["Value"]
    
    print({"firstName":fname,"lastName":lname})
    
    return {
        'statusCode': 200,
        'body': json.dumps({"firstName":fname,"lastName":lname})
    }
    
