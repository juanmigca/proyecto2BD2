from utils.models import MenuItem
from utils.utilsApi import serialize_document

def queryBuilder(ids = None, ingredients = None, name = None):
    args = {}
    if ids is not None:
        if isinstance(ids, list) and len(ids) > 1:
            args['id'] = {"$in": [int(i) for i in ids]}
        elif isinstance(ids, list) and len(ids) == 1:
            args['id'] = int(ids[0])
        else:
            args['id'] = int(ids)
    if name is not None:
        if isinstance(name, list) and len(name) > 1:
            args['name'] = {"$in": [r for r in name]}
        elif isinstance(name, list) and len(name) == 1:
            args['name'] = name[0]
        else:
            args['name'] = name
    return args
    
    
    
def getMenuItems(collection, ids = None, name = None, limit = None, sort = "addedToMenu"):
    args = queryBuilder(ids, name)
    print(args)
    if limit is not None:
        result = collection.find(args).sort(sort).limit(limit)
    else:
        result = collection.find(args).sort(sort)
    menuItems = []
    for item in result:
        menuItems.append(serialize_document(item))
        
    #print(result)
    return list(menuItems)

def createMenuItem(collection, menu_item):
    """
    Creates a new menu item in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    
    menu_item_dict = menu_item.model_dump()
    existing_menu_item = collection.find_one({"id": menu_item_dict["id"]})
    if existing_menu_item:
        raise ValueError ("Menu Item already exists")  
    
    result = collection.insert_one(menu_item_dict)
    return {"inserted_id": str(result.inserted_id)}

def createMultipleMenuItem(collection,menu_items):
    """
    Creates multiple menu items in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    menu_items_dict = menu_items.model_dump() 
    result = collection.insert_many(menu_items_dict)
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}

def updateMenuItem(collection, id, menu_item):
    """
    Updates an existing menu item in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    menu_item_dict = menu_item.model_dump()
    menu_item_dict = {k: v for k, v in menu_item_dict.items() if v is not None}  
    result = collection.update_one({"id": int(id)}, {"$set": menu_item_dict})
    if result.matched_count == 0:
        raise ValueError(f"Menu item with id {id} not found.")
    return {"modified_count": result.modified_count}

def updateMultipleMenuItem(collection, ids, menu_items):
    """
    Updates multiple menu items in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    menu_item_dict = menu_items.model_dump()
    menu_item_dict = {k: v for k, v in menu_item_dict.items() if v is not None}
    result = collection.update_many({"id": {"$in": [int(i) for i in ids]}}, {"$set": menu_item_dict})
    return {"modified_count": result.modified_count}

def deleteMenuItem(collection, id):
    """
    Deletes a menu item from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"id": int(id)})
    if result.deleted_count == 0:
        raise ValueError(f"Menu item with id {id} not found.")
    return {"deleted_count": result.deleted_count}

def deleteMultipleMenuItems(collection,ids):
    """
    Deletes multiple menu items from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"id": {"$in": [int(i) for i in ids]}})
    return {"deleted_count": result.deleted_count}
