import json
import boto3
import os
import urllib.parse

sfn = boto3.client('stepfunctions')
STATE_MACHINE_ARN = os.environ['STATE_MACHINE_ARN']

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    try:
        # Handle S3 event or direct JSON body
        bucket = None
        key = None

        if 'Records' in event and event['Records'][0].get('s3'):
            rec = event['Records'][0]['s3']
            bucket = rec['bucket']['name']
            key = rec['object']['key']
        else:
            body = event.get('body')
            if isinstance(body, str):
                body = json.loads(body)
            else:
                body = body or event

            bucket = body.get('bucket')
            key = body.get('key')

        if not bucket or not key:
            return {"status": "FAILURE", "error": "missing bucket/key"}

        input_payload = json.dumps({"bucket": bucket, "key": key})
        resp = sfn.start_execution(stateMachineArn=STATE_MACHINE_ARN, input=input_payload)
        return {"status": "STARTED", "executionArn": resp.get('executionArn')}

    except Exception as e:
        return {"status": "FAILURE", "error": str(e)}
