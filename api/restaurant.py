import pymongo
from models import Restaurant
    
def queryBuilder(id = None, name = None, cuisines = None):
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
    if cuisines is not None:
        if isinstance(cuisines, list):
            args['cuisines'] = {"$in": [cuisine for cuisine in cuisines]}
        else:
            args['cuisines'] = cuisines
        
    return args


def getRestaurants(collection, id = None, name = None, cuisines = None):
    """
    Returns a list of restaurants.
    """
    
    restaruant_collection = collection
    if restaruant_collection is None:
        raise ValueError
    args = queryBuilder(id, name, cuisines)
  
    restaurants = restaruant_collection.find(args)
    return list(restaurants)

def createRestaurant(collection, restaurant):
    
    if collection is None:
        return None
    
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
        return None
    
    update_data = {k: v for k, v in restaurant.dict(exclude_unset=True).items() if v is not None}

    if not update_data:
        return None

    result = collection.update_one(
        {"id": id},           
        {"$set": update_data} 
    )

    return result.modified_count
    

    


    
        
        
    

    