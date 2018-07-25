import time
import json
from sender import send_json, remove_json, create_mongo_client, get_collection


def set_reconcile(src_seq, dst_seq, dbname, collection):
    "Return required operations to mutate src_seq into dst_seq"
    src_set= set(src_seq) # no-op if already of type set
    dst_set= set(dst_seq) # ditto

    for item in src_set - dst_set:
        print('Removing Item: ' + item)
        remove_json(json.loads(item), dbname, collection)

    for item in dst_set - src_set:
        print('Adding Item: ' + item)
        send_json(json.loads(item), dbname, collection)

def sync_data(filepath):
    # Read File
    data_to_sync = [line.rstrip('\n') for line in open(filepath)]

    # Read Collection
    dbname = 'sandbox'
    collection = 'test_collection'
    posts = list(get_collection(dbname, collection).find())
    posts = ['{"id":"' + item['id'] + '"}' for item in posts]

    # Sync all of the data
    set_reconcile(posts, data_to_sync, dbname, collection)


filepath = 'data'

while True:
    print('Syncing data...')
    sync_data(filepath)
    print('Sync complete! Waiting...')
    time.sleep(5)