from utils.models import Cuisines
from bson import ObjectId
from utils.utilsApi import serialize_document

def query_builder(id=None,name=None):
    """
    Builds a query for MongoDB based on the provided parameters.
    """
    args = {}
    if id is not None:
        if isinstance(id, list) and len(id) > 1:
            args['id'] = {"$in": [int(i) for i in id]}
        elif isinstance(id, list) and len(id) == 1:
            args['id'] = int(id[0])
        else:
            args['id'] = int(id)
    if name is not None:
        if isinstance(name, list) and len(name) > 1:
            args['name'] = {"$in": [name for name in name]}
        elif isinstance(name, list) and len(name) == 1:
            args['name'] = name[0]
        else:
            args['name'] = name
    return args

def getCuisine(collection, id=None, name=None, limit=10, sort="name"):
    """
    Returns a list of cuisines based on the provided parameters.
    """
    if collection is None:
        raise ValueError('Collection is None')
    
    args = query_builder(id, name)
    if limit is not None:
        cursor = collection.find(args).sort(sort).limit(limit)
    else:
        cursor = collection.find(args).sort(sort)

    cuisines = []
    for cuisine in cursor:
        cuisines.append(serialize_document(cuisine))
    return list(cuisines)

def createCuisine(collection, cuisine=Cuisines):
    """
    Creates a new cuisine in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    cuisine_dict = cuisine.model_dump()
    new_id = collection.find_one({}, sort=[("id", -1)]).get("id", 0) + 1
    cuisine_dict["id"] = new_id
    result = collection.insert_one(cuisine_dict)
    return {"inserted_id": str(result.inserted_id)}

def createMultipleCuisine(collection, cuisine=Cuisines):
    """
    Creates multiple cuisines in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    cuisines_dict = cuisine.model_dump() 
    new_id = collection.find_one({}, sort=[("id", -1)]).get("id", 0) + 1
    cuisines_dict["id"] = new_id
    result = collection.insert_many(cuisines_dict)
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}

def updateCuisine(collection, id, cuisine=Cuisines):
    """
    Updates a cuisine in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    cuisine_dict = cuisine.model_dump()
    cuisine_dict = {k: v for k, v in cuisine_dict.items() if v is not None}  
    result = collection.update_one({"id": int(id)}, {"$set": cuisine_dict})
    if result.modified_count == 0:
        raise ValueError("Cuisine not found or no changes made")
    return {"modified_count": result.modified_count}

def updateMultipleCuisine(collection, ids, cuisine=Cuisines):
    """
    Updates multiple cuisines in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    cuisine_dict = cuisine.model_dump()
    cuisine_dict = {k: v for k, v in cuisine_dict.items() if v is not None} 
    result = collection.update_many({"id": {"$in": [int(id) for id in ids]}}, {"$set": cuisine_dict})
    if result.modified_count == 0:
        raise ValueError("Cuisines not found or no changes made")
    return {"modified_count": result.modified_count}

def deleteCuisine(collection, id):
    """
    Deletes a cuisine from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"id": int(id)})
    if result.deleted_count == 0:
        raise ValueError("Cuisine not found")
    return {"deleted_count": result.deleted_count}

def deleteMultipleCuisine(collection, ids):
    """
    Deletes multiple cuisines from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"id": {"$in": [int(id) for id in ids]}})
    if result.deleted_count == 0:
        raise ValueError("Cuisines not found")
    return {"deleted_count": result.deleted_count}
    