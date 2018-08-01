
from pymongo import MongoClient

def create_mongo_client():
    connection_string = 'mongodb://mnemicdb:SSk5W27TVjblhrCrsq25w1rQfFiCDrZs7Nk6SXFSvHav5G11P7TLt8iqMovRSlCBvrrSblzI2pnalMAHrDAaXw==@mnemicdb.documents.azure.com:10255/?ssl=true&replicaSet=globaldb'
    client = MongoClient(connection_string)

    return client


def get_collection(dbname, collection):
    # Create Client and DB
    client = create_mongo_client()
    db = client[dbname]
    posts = db[collection]

    return posts

def send_json(json, dbname, collection):
    posts = get_collection(dbname, collection)
    result = posts.insert_one(json)
    return result

def remove_json(json, dbname, collection):
    posts = get_collection(dbname, collection)
    result = posts.remove(json, True)
    return result
