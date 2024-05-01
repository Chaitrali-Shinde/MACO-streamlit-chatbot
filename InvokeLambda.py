import boto3
from log_setup import logger
import json
import os

def lambda_handler(event, context):
    
    functionName = os.environ['FUNCTION_NAME']
    invocation_type = 'RequestResponse'

    payload = {
        "question": event["question"]
    }

    client = boto3.client('lambda')
    try:
        response = client.invoke(
            FunctionName= functionName,
            InvocationType= invocation_type,
            Payload=json.dumps(payload)
            )
        
        responseBody = json.loads(response['Payload'].read())['body']
        if responseBody.startswith('"') and responseBody.endswith('"'):
            responseBody = responseBody[1:-1]
            
        return { 
            "status_code": 200,
            "body": json.dumps({"response": responseBody})
        }
    except Exception as e:
        logger.debug(e)
        return {
            "status_code": 500,
            "body": json.dumps({"response": str(e)})  # "error": "Internal Server Error"
        }
