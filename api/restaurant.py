import pymongo
from models import Restaurant
from bson import ObjectId

def serialize_restaurant(restaurant):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    restaurant["_id"] = str(restaurant["_id"])
    return restaurant

    
def queryBuilder(id = None, name = None, cuisine = None):
    args = {}
    if id is not None:
        if isinstance(id, list):
            args['id'] = {"$in": [i for i in id]}
        else:
            args['id'] = id
    if name is not None:
        if isinstance(name, list):
            args['name'] = {"$in": [n for n in name]}
        else:
            args['name'] = name
    if cuisine is not None:
        if isinstance(cuisine, list):
            args['cuisines'] = {"$in": [cuisine for cuisine in cuisine]}
        else:
            args['cuisines'] = cuisine
        
    return args


def getRestaurants(collection, id = None, name = None, cuisine = None):
    """
    Returns a list of restaurants.
    """

    if collection is None:
        raise ValueError('Collection is None')
    args = queryBuilder(id, name, cuisine)
    print(args)
    cursor = collection.find(args).limit(10)
    restaurants = []
    for restaurant in cursor:
        restaurants.append(serialize_restaurant(restaurant))

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
    

    


    
        
        
    

    