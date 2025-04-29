from models import MenuItem
from bson import ObjectId

def serialize_document(menu_item=MenuItem):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    menu_item["_id"] = str(menu_item["_id"])
    return menu_item

def queryBuilder(id=None,name=None,price=None,ingredients=None):
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
    if price is not None:
        if isinstance(price, list) and len(price) > 1:
            args['price'] = {"$in": [float(price) for price in price]}
        elif isinstance(price, list) and len(price) == 1:
            args['price'] = float(price[0])
        else:
            args['price'] = float(price)
    if ingredients is not None:
        if isinstance(ingredients, list) and len(ingredients) > 1:
            args['ingredients'] = {"$in": [ingredients for ingredients in ingredients]}
        elif isinstance(ingredients, list) and len(ingredients) == 1:
            args['ingredients'] = ingredients[0]
        else:
            args['ingredients'] = ingredients
    return args

def get_menu_item(collection, id=None, name=None, price=None, ingredients=None, limit=10):
    """
    Returns a list of menu items based on the provided parameters.
    """
    if collection is None:
        raise ValueError('Collection is None')
    args = queryBuilder(id, name, price, ingredients)
    cursor = collection.find(args).limit(limit)
    menu_items = []
    for menu_item in cursor:
        menu_items.append(serialize_document(menu_item))
    return list(menu_items)

def create_menu_item(collection, menu_item=MenuItem):
    """
    Creates a new menu item in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    menu_item_dict=menu_item.model_dump()
    existing_menu_item = collection.find_one({"_id": menu_item_dict["_id"]})
    if existing_menu_item:
        raise ValueError ("Menu Item already exists")  # Item already exists, return None or handle as needed
    result = collection.insert_one(menu_item)
    return {"inserted_id": id(result.inserted_id)}

def create_multiple_menu_item(collection,menu_items=MenuItem):
    """
    Creates multiple menu items in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    menu_items_dict = [menu_item.model_dump() for menu_item in menu_items]
    result = collection.insert_many(menu_items_dict)
    return {"inserted_ids": [int(id) for id in result.inserted_ids]}

def update_menu_item(collection, id, menu_item=MenuItem):
    """
    Updates an existing menu item in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    menu_item_dict = menu_item.model_dump()
    result = collection.update_one({"_id": int(id)}, {"$set": menu_item_dict})
    if result.matched_count == 0:
        raise ValueError(f"Menu item with id {id} not found.")
    return {"modified_count": result.modified_count}

def multiple_menu_item(collection, ids, menu_items=MenuItem):
    """
    Updates multiple menu items in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    menu_item_dict = menu_items.model_dump()
    result = collection.update_many({"_id": {"$in": [int(i) for i in ids]}}, {"$set": menu_item_dict})
    return {"modified_count": result.modified_count}

def delete_menu_item(collection, id):
    """
    Deletes a menu item from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"_id": int(id)})
    if result.deleted_count == 0:
        raise ValueError(f"Menu item with id {id} not found.")
    return {"deleted_count": result.deleted_count}

def delete_multiple_menu_items(collection,ids):
    """
    Deletes multiple menu items from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"_id": {"$in": [int(i) for i in ids]}})
    return {"deleted_count": result.deleted_count}