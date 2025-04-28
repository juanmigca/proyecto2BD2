import pymongo
from models import Order
from bson import ObjectId
def serialize_document(order=Order):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    order["_id"] = str(order["_id"])
    return order
def queryBuilder(id=None,user_id=None,restaurant_id=None,status=None):
    args = {}
    if id is not None:
        if isinstance(id, list) and len(id) > 1:
            args['_id'] = {"$in": [int(i) for i in id]}
        elif isinstance(id, list) and len(id) == 1:
            args['_id'] = int(id[0])
        else:
            args['_id'] = int(id)
    if user_id is not None:
        if isinstance(user_id, list) and len(user_id) > 1:
            args['userId'] = {"$in": [int(user_id) for user_id in user_id]}
        elif isinstance(user_id, list) and len(user_id) == 1:
            args['userId'] = int(user_id[0])
        else:
            args['userId'] = int(user_id)
    if restaurant_id is not None:
        if isinstance(restaurant_id, list) and len(restaurant_id) > 1:
            args['restaurantId'] = {"$in": [int(restaurant_id) for restaurant_id in restaurant_id]}
        elif isinstance(restaurant_id, list) and len(restaurant_id) == 1:
            args['restaurantId'] = int(restaurant_id[0])
        else:
            args['restaurantId'] = int(restaurant_id)
    if status is not None:
        if isinstance(status, list) and len(status) > 1:
            args['status'] = {"$in": [status for status in status]}
        elif isinstance(status, list) and len(status) == 1:
            args['status'] = status[0]
        else:
            args['status'] = status
    return args
def getOrders(collection, id=None, user_id=None, restaurant_id=None, status=None, limit=10):
    """
    Returns a list of orders.
    """
    if collection is None:
        raise ValueError('Collection is None')
    args = queryBuilder(id, user_id, restaurant_id, status)
    cursor = collection.find(args).limit(limit)
    orders = []
    for order in cursor:
        orders.append(serialize_document(order))
    return list(orders)
def createOrder(collection, order=Order):
    """
    Creates a new order in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    order_dict = order.model_dump()
    existing_order = collection.find_one({"_id": order_dict["_id"]})
    if existing_order:
        raise ValueError(f"Order with id {order_dict['_id']} already exists.")
    result = collection.insert_one(order_dict)
    return {"inserted_id": str(result.inserted_id)}
def updateOrder(collection, id, order):
    """
    Updates an existing order in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    existing_order = collection.find_one({"_id": ObjectId(id)})
    if not existing_order:
        raise ValueError(f"Order with id {id} does not exist.")
    update_fields = {k: v for k, v in order.dict(exclude_unset=True).items() if v is not None}
    if not update_fields:
        raise ValueError("No fields to update.")
    result = collection.update_one({"_id": (id)}, {"$set": update_fields})
    return {"modified_count": result.modified_count}
def updateMultipleOrders(collection, ids, order=Order):
    """
    Updates multiple orders in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    if not ids:
        raise ValueError("No ids provided.")
    update_fields = {k: v for k, v in order.dict(exclude_unset=True).items() if v is not None}
    if not update_fields:
        raise ValueError("No fields to update.")
    result = collection.update_many({"_id": {"$in": [int(id) for id in ids]}}, {"$set": update_fields})
    return {"modified_count": result.modified_count}
def deleteOrder(collection, id):
    """
    Deletes an order from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"_id": int(id)})
    return {"deleted_count": result.deleted_count}
def deleteMultipleOrders(collection, ids):
    """
    Deletes multiple orders from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"_id": {"$in": [int(id) for id in ids]}})
    return {"deleted_count": result.deleted_count}
