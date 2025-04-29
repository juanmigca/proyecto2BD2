import pymongo
from models import Restaurant
from bson import ObjectId
from utilsApi import serialize_document


    
def queryBuilder(id = None, name = None, cuisine = None):
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
            args['name'] = {"$in": [n for n in name]}
        elif isinstance(name, list) and len(name) == 1:
            args['name'] = name[0]
        else:
            args['name'] = name
    if cuisine is not None:
        if isinstance(cuisine, list) and len(cuisine) > 1:
            args['cuisines'] = {"$in": [cuisine for cuisine in cuisine]}
        elif isinstance(cuisine, list) and len(cuisine) == 1:
            args['cuisines'] = cuisine[0]
        else:
            args['cuisines'] = cuisine
    
        
    return args


def getRestaurants(collection, id = None, name = None, cuisine = None, limit = 10, sort = "rating"):
    """
    Returns a list of restaurants.
    """
    
    if collection is None:
        raise ValueError('Collection is None')
    args = queryBuilder(id, name, cuisine)
    print(args)
    
    cursor = collection.find(args).sort(sort).limit(limit)
    restaurants = []
    for restaurant in cursor:
        restaurants.append(serialize_document(restaurant))

    return list(restaurants)

def createRestaurant(collection, restaurant):
    
    if collection is None:
        raise ValueError('Collection is None')
    
    restaurant_dict = restaurant.dict()
    
    existing = collection.find_one({"id": restaurant_dict["id"]})
    if existing:
        raise ValueError('Restaurant with that id already exists')

  
    result = collection.insert_one(restaurant_dict)

    return {"inserted_id": str(result.inserted_id)}
    
    
    
def updateRestaurant(collection, id, restaurant):
    """
    Updates a restaurant.
    """
    
    if collection is None:
        raise ValueError('Collection is None')
    
    update_data = {k: v for k, v in restaurant.dict(exclude_unset=True).items() if v is not None}

    if not update_data:
        return None

    result = collection.update_one(
        {"id": id},           
        {"$set": update_data} 
    )

    return result.modified_count

def updateMultipleRestaurants(collection, ids, restaurants):
    """
    Updates multiple restaurants.
    """
    
    if collection is None:
        raise ValueError('Collection is None')
    
    update_data = {k: v for k, v in restaurants.dict(exclude_unset=True).items() if v is not None}

    if not update_data:
        return None

    result = collection.update_many(
        {"id": {"$in": ids}},           
        {"$set": update_data} 
    )

    return result.modified_count
 

    
def getCuisines(collection):
    """
    Returns a list of cuisines.
    """
    
    if collection is None:
        raise ValueError('Collection is None')
    
    cursor = collection.find()
    cuisines = []
    for cuisine in cursor:
        cuisines.append(serialize_document(cuisine))

    return list(cuisines)

def deleteRestaurant(collection, id):
    if collection is None:
        raise ValueError('Collection is None')
    
    result = collection.delete_one({"id": id})
    
    return result.deleted_count


def deletemultipleRestaurants(collection, ids):
    if collection is None:
        raise ValueError('Collection is None')
    
    result = collection.delete_many({"id": {"$in": ids}})
    
    return result.deleted_count
