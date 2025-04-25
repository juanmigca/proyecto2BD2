import pymongo


    
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

    
    
    
    
    
    
    
        
        
    

    