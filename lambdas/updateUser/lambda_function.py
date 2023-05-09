import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    
    userId = event['pathParameters']['userId']
    
    userObject = json.loads(event['body'])
    
    print(userObject)
    
    cognitoClient = boto3.client('cognito-idp')
    try:
        response = cognitoClient.admin_update_user_attributes(
            UserPoolId='us-east-1_C8J5HLL6q',
            Username=userId,
            UserAttributes=[
                {
                    'Name': 'custom:tags',
                    'Value': userObject['custom:tags']
                }
            ]
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(userObject)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode' : 500,
            'body' : json.dumps(userObject)
        }
