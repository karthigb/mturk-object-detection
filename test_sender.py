from sender import send_json, create_mongo_client

dbname = 'sandbox'
collection = 'test_collection'

json = {
    'name': 'Cley',
    'address': '123 Fake St',
    'phone': '1-800-94JENNY'
}

result = send_json(json, dbname, collection)