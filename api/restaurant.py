import pymongo
from utils import getCollection


    
def queryBuilder(id = None, name = None, cuisines = None):
    
    
    
    args = {}
    if id is not None:
        args['id'] = id
    if name is not None:
        args['name'] = name
    if cuisines is not None:
        if isinstance(cuisines, list):
            args['cuisines'] = {"$in": [cuisine for cuisine in cuisines]}
        else:
            args['cuisines'] = cuisines
        
    return args

def getRestaurants(id = None, name = None, cuisines = None):
    """
    Returns a list of restaurants.
    """
    
    restaruant_collection = getCollection('proyecto2bd', 'restaurants')
    if restaruant_collection is None:
        return None
    args = queryBuilder(id, name, cuisines)
  
    restaurants = restaruant_collection.find(args)
    return list(restaurants)
 
    
    
    
    
    
    
    
        
        
    

    