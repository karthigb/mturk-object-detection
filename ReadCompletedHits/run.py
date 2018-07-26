import os
import json

from sender import send_json, remove_json, create_mongo_client, get_collection

# Read Active Hits from Cosmos
result = list(get_collection('sandbox', 'completed_hits').find())
print("Getting Completed Hits...")

# Create JSON Payload
active_hits = []

for item in result:
    data = {
        'id': item['id'],
        'group_id': item['group_id'],
        'url': item['url'],
        'value': item['value']
    }
    print("Got Hit id:" + item['id'] + ", group_id:" + item['group_id'] + ", url:" + item['url'])
    active_hits.append(data)

payload = {
    'completed_hits': active_hits
}
json_array = json.dumps(payload)

# Write JSON Payload as response
response = open(os.environ['res'], 'w')
response.write(json_array)
response.close()