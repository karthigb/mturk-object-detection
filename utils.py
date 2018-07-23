import boto3
import json

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

def get_mturk_client():
    with open('config.json', 'r') as f:
        config = json.load(f)

    mturk = boto3.client('mturk',
       aws_access_key_id = config['SANDBOX']['aws_access_key_id'],
       aws_secret_access_key = config['SANDBOX']['aws_secret_access_key'],
       region_name='us-east-1',
       endpoint_url = MTURK_SANDBOX
    )

    return mturk
