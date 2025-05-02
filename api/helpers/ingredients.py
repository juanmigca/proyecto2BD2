from utils.models import Ingredient
from bson import ObjectId

def serialize_document(ingredient=Ingredient):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    ingredient["_id"] = str(ingredient["_id"])
    return ingredient

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

def get_ingredient(collection, name=None, amount=None, unitMeasure=None, limit=10):
    """
    Returns a list of ingredients based on the provided parameters.
    """
    if collection is None:
        raise ValueError('Collection is None')
    args = queryBuilder(name, amount, unitMeasure)
    cursor = collection.find(args).limit(limit)
    ingredients = []
    for ingredient in cursor:
        ingredients.append(serialize_document(ingredient))
    return list(ingredients)

def create_ingredient(collection, ingredient=Ingredient):
    """
    Creates a new ingredient in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    ingredient_dict = ingredient.model_dump()
    existing_ingredient = collection.find_one({"_id": ingredient_dict["_id"]})
    if existing_ingredient:
        raise ValueError("Ingredient already exists")  # Item already exists, return None or handle as needed
    result = collection.insert_one(ingredient_dict)
    return {"inserted_id": str(result.inserted_id)}

def create_multiple_ingredient(collection, ingredient=Ingredient):
    """
    Creates multiple ingredients in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    ingredient_dict = ingredient.model_dump() 
    result = collection.insert_many(ingredient_dict)
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}

def update_ingredient(collection, ingredient=Ingredient):
    """
    Updates an existing ingredient in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    ingredient_dict = ingredient.model_dump()
    result = collection.update_one({"name": (ingredient_dict["name"])}, {"$set": ingredient_dict})
    return {"modified_count": result.modified_count}

def multiple_update_ingredient(collection,names,ingredients=Ingredient):
    """
    Updates multiple ingredients in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    ingredients_dict = ingredients.model_dump()
    result = collection.update_many({"name": {"$in": [ name for name in names]}}, {"$set": ingredients_dict})
    return {"modified_count": result.modified_count}

def delete_ingredient(collection, id):
    """
    Deletes an ingredient from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"_id": ObjectId(id)})
    return {"deleted_count": result.deleted_count}

def delete_multiple_ingredient(collection, ids):
    """
    Deletes multiple ingredients from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"_id": {"$in": [ObjectId(id) for id in ids]}})
    return {"deleted_count": result.deleted_count}