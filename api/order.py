import pymongo
from models import Order
from bson import ObjectId
def serialize_document(order):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    order["_id"] = str(order["_id"])
    return order
def queryBuilder(id=None,user_id=None,restaurant_id=None,status=None):
    args = {}
    if id is not None:
        if isinstance(id, list) and len(id) > 1:
            args['_id'] = {"$in": [ObjectId(i) for i in id]}
        elif isinstance(id, list) and len(id) == 1:
            args['_id'] = ObjectId(id[0])
        else:
            args['_id'] = ObjectId(id)
    if user_id is not None:
        if isinstance(user_id, list) and len(user_id) > 1:
            args['userId'] = {"$in": [user_id for user_id in user_id]}
        elif isinstance(user_id, list) and len(user_id) == 1:
            args['userId'] = user_id[0]
        else:
            args['userId'] = user_id
    if restaurant_id is not None:
        if isinstance(restaurant_id, list) and len(restaurant_id) > 1:
            args['restaurantId'] = {"$in": [restaurant_id for restaurant_id in restaurant_id]}
        elif isinstance(restaurant_id, list) and len(restaurant_id) == 1:
            args['restaurantId'] = restaurant_id[0]
        else:
            args['restaurantId'] = restaurant_id
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
def createOrder(collection, order):
    """
    Creates a new order in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    order_dict = order.dict()
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
    order_dict = order.dict()
    existing_order = collection.find_one({"_id": ObjectId(id)})
    if not existing_order:
        raise ValueError(f"Order with id {id} does not exist.")
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": order_dict})
    return {"modified_count": result.modified_count}
   
