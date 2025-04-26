from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

URI = "mongodb+srv://raul:pauwrauw@lab05.yt4up.mongodb.net/?retryWrites=true&w=majority&appName=lab05"

def getMongoClient():
    """
    Returns a MongoDB client.
    """
    try:
        client = MongoClient(URI, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            return None
        print("Connected to MongoDB")
        return client
    except:
        print("Error connecting to MongoDB")    
        return None

def getDatabase(client, db_name):
    """
    Returns a MongoDB database.
    """
    if client is None:
        print("Error connecting to MongoDB")
        return None
    try:
        db = client[db_name]
        return db
    except:
        print("Error connecting to MongoDB")
        return None 
    
def getCollection(client, db_name, collection_name):
    """
    Returns a MongoDB collection.
    """
    
    db = getDatabase(client, db_name)
    if db is None:
        return None
    
    try:
        collection = db[collection_name]
        return collection
    except:
        print("Error connecting to MongoDB")
        return None
    
    
    
