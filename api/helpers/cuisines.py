from utils.models import Cuisines
from bson import ObjectId

def serialize_document(cuisine=Cuisines):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    cuisine["_id"] = int(cuisine["_id"])
    return cuisine

def query_builder(id=None,name=None):
    """
    Builds a query for MongoDB based on the provided parameters.
    """
    args = {}
    if id is not None:
        if isinstance(id, list) and len(id) > 1:
            args['_id'] = {"$in": [int(i) for i in id]}
        elif isinstance(id, list) and len(id) == 1:
            args['_id'] = int(id[0])
        else:
            args['_id'] = int(id)
    if name is not None:
        if isinstance(name, list) and len(name) > 1:
            args['name'] = {"$in": [name for name in name]}
        elif isinstance(name, list) and len(name) == 1:
            args['name'] = name[0]
        else:
            args['name'] = name
    return args

def get_cuisine(collection, id=None, name=None, limit=10):
    """
    Returns a list of cuisines based on the provided parameters.
    """
    if collection is None:
        raise ValueError('Collection is None')
    args = query_builder(id, name)
    cursor = collection.find(args).limit(limit)
    cuisines = []
    for cuisine in cursor:
        cuisines.append(serialize_document(cuisine))
    return list(cuisines)

def create_cuisine(collection, cuisine=Cuisines):
    """
    Creates a new cuisine in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    cuisine_dict = cuisine.model_dump()
    existing_cuisine = collection.find_one({"_id": cuisine_dict["_id"]})
    if existing_cuisine:
        raise ValueError("Cuisine already exists")  # Item already exists, return None or handle as needed
    result = collection.insert_one(cuisine_dict)
    return {"inserted_id": str(result.inserted_id)}

def create_multiple_cuisine(collection, cuisine=Cuisines):
    """
    Creates multiple cuisines in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    cuisines_dict = cuisine.model_dump() 
    result = collection.insert_many(cuisines_dict)
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}

def update_cuisine(collection, id, cuisine=Cuisines):
    """
    Updates a cuisine in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    cuisine_dict = cuisine.model_dump()
    result = collection.update_one({"_id": int(id)}, {"$set": cuisine_dict})
    if result.modified_count == 0:
        raise ValueError("Cuisine not found or no changes made")
    return {"modified_count": result.modified_count}

def update_multiple_cuisine(collection, ids, cuisine=Cuisines):
    """
    Updates multiple cuisines in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    cuisine_dict = cuisine.model_dump()
    result = collection.update_many({"_id": {"$in": [int(id) for id in ids]}}, {"$set": cuisine_dict})
    if result.modified_count == 0:
        raise ValueError("Cuisines not found or no changes made")
    return {"modified_count": result.modified_count}

def delete_cuisine(collection, id):
    """
    Deletes a cuisine from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"_id": int(id)})
    if result.deleted_count == 0:
        raise ValueError("Cuisine not found")
    return {"deleted_count": result.deleted_count}

def delete_multiple_cuisine(collection, ids):
    """
    Deletes multiple cuisines from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"_id": {"$in": [int(id) for id in ids]}})
    if result.deleted_count == 0:
        raise ValueError("Cuisines not found")
    return {"deleted_count": result.deleted_count}
    