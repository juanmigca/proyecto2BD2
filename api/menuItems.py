from models import MenuItem
from utilsApi import serialize_document

def queryBuilder(ids = None, ingredients = None, restaurants = None):
    args = {}
    if ids is not None:
        if isinstance(ids, list) and len(ids) > 1:
            args['id'] = {"$in": [int(i) for i in ids]}
        elif isinstance(ids, list) and len(ids) == 1:
            args['id'] = int(ids[0])
        else:
            args['id'] = int(ids)
    if ingredients is not None:
        if isinstance(ingredients, list) and len(ingredients) > 1:
            args['ingredients.name'] = {"$in": [i for i in ingredients]}
        elif isinstance(ingredients, list) and len(ingredients) == 1:
            args['ingredients.name'] = ingredients[0]
        else:
            args['ingredients.name'] = ingredients
    if restaurants is not None:
        if isinstance(restaurants, list) and len(restaurants) > 1:
            args['restaurantId'] = {"$in": [r for r in restaurants]}
        elif isinstance(restaurants, list) and len(restaurants) == 1:
            args['restaurantId'] = restaurants[0]
        else:
            args['restaurantId'] = restaurants
    return args
    
    
    
def getMenuItems(collection, ids = None, ingredients = None, restaurants = None, limit = None, sort = "addedToMenu"):
    args = queryBuilder(ids, ingredients, restaurants)
    print(args)
    if limit is not None:
        result = collection.find(args).sort(sort).limit(limit)
    else:
        result = collection.find(args).sort(sort)
    menuItems = []
    for item in result:
        menuItems.append(serialize_document(item))
        
    print(result)
    return list(menuItems)

