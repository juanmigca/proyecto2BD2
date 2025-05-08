from utils.models import Ingredient
from bson import ObjectId
from utils.utilsApi import serialize_document

def queryBuilder(name=None,amount=None,unitMeasure=None):
    """
    Builds a query for MongoDB based on the provided parameters.
    """
    args = {}
    if name is not None:
        if isinstance(name, list) and len(name) > 1:
            args['name'] = {"$in": [name for name in name]}
        elif isinstance(name, list) and len(name) == 1:
            args['name'] = name[0]
        else:
            args['name'] = name
    if amount is not None:
        if isinstance(amount, list) and len(amount) > 1:
            args['amount'] = {"$in": [float(amount) for amount in amount]}
        elif isinstance(amount, list) and len(amount) == 1:
            args['amount'] = float(amount[0])
        else:
            args['amount'] = float(amount)
    if unitMeasure is not None:
        if isinstance(unitMeasure, list) and len(unitMeasure) > 1:
            args['unitMeasure'] = {"$in": [unitMeasure for unitMeasure in unitMeasure]}
        elif isinstance(unitMeasure, list) and len(unitMeasure) == 1:
            args['unitMeasure'] = unitMeasure[0]
        else:
            args['unitMeasure'] = unitMeasure
    return args

def getIngredients(collection, name=None, amount=None, unitMeasure=None, limit=10, sort="name"):
    """
    Returns a list of ingredients based on the provided parameters.
    """
    if collection is None:
        raise ValueError('Collection is None')
        
    args = queryBuilder(name, amount, unitMeasure)
    if limit is not None:
        cursor = collection.find(args).sort(sort).limit(limit)
    else:
        cursor = collection.find(args).sort(sort)
    ingredients = []
    for ingredient in cursor:
        ingredients.append(serialize_document(ingredient))
    return list(ingredients)

def createIngredient(collection, ingredient=Ingredient):
    """
    Creates a new ingredient in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    ingredient_dict = ingredient.model_dump()

   
        
    result = collection.insert_one(ingredient_dict)
    return {"inserted_id": str(result.inserted_id)}

def createMultipleIngredient(collection, ingredient=Ingredient):
    """
    Creates multiple ingredients in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    ingredient_dict = ingredient.model_dump() 
    result = collection.insert_many(ingredient_dict)
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}

def updateIngredient(collection, name, ingredient=Ingredient):
    """
    Updates an existing ingredient in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    ingredient_dict = ingredient.model_dump()
    ingredient_dict = {k: v for k, v in ingredient_dict.items() if v is not None}
    result = collection.update_one({"name": name}, {"$set": ingredient_dict})
    return {"modified_count": result.modified_count}

def multipleUpdateIngredient(collection,names,ingredients=Ingredient):
    """
    Updates multiple ingredients in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    ingredients_dict = ingredients.model_dump()
    ingredient_dict = {k: v for k, v in ingredient_dict.items() if v is not None}
    result = collection.update_many({"name": {"$in": [name for name in names]}}, {"$set": ingredients_dict})
    return {"modified_count": result.modified_count}

def deleteIngredient(collection, name):
    """
    Deletes an ingredient from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"name": name})
    return {"deleted_count": result.deleted_count}

def deleteMultipleIngredient(collection, names):
    """
    Deletes multiple ingredients from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"name": {"$in": [name for name in names]}})
    return {"deleted_count": result.deleted_count}