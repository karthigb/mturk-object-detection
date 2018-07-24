import boto3

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
mturk = boto3.client('mturk',
   aws_access_key_id = "AKIAJDHFOV2PPA7KBNQA",
   aws_secret_access_key = "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",
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)

response = mturk.delete_hit(
    HITId='3X0EMNLXEPPPR1QA1QES6EA0ZZ5PVT'
)

print "A new HIT has been created. You can preview it here:"
print response['HIT']