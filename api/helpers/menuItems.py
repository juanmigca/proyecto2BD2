from utils.models import MenuItem
from utils.utilsApi import serialize_document

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
    return {"inserted_id": (result.inserted_id)}

def create_multiple_menu_item(collection,menu_items=MenuItem):
    """
    Creates multiple menu items in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    menu_items_dict = menu_items.model_dump() 
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
