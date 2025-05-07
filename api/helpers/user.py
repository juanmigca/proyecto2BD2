from utils.models import User
from bson import ObjectId

from utils.utilsApi import serialize_document

def queryBuilder(id=None, username=None, order_mode="equals", numOrders=None, review_mode="equals", numReviews=None, visitedRestaurants=None):
    """
    Builds a query for MongoDB based on the provided parameters.
    """
    args = {}
    if id is not None:
        if isinstance(id, list) and len(id) > 1:
            args['id'] = {"$in": [int(i) for i in id]}
        elif isinstance(id, list) and len(id) == 1:
            args['id'] = int(id[0])
        else:
            args['id'] = int(id)
    if username is not None:
        if isinstance(username, list) and len(username) > 1:
            args['username'] = {"$in": [username for username in username]}
        elif isinstance(username, list) and len(username) == 1:
            args['username'] = username[0]
        else:
            args['username'] = username
    if numOrders is not None:
        
        if order_mode == "greater":
            args['numOrders'] = {"$gt": int(numOrders[0])}
        elif order_mode == "lesser":
            args['numOrders'] = {"$lt": int(numOrders[0])}
        elif order_mode == "equals":
            if isinstance(numOrders, list) and len(numOrders) > 1:
                args['numOrders'] = {"$in": [int(numOrders) for numOrders in numOrders]}
            elif isinstance(numOrders, list) and len(numOrders) == 1:
                args['numOrders'] = int(numOrders[0])
            else:
                args['numOrders'] = int(numOrders)
    if numReviews is not None:
        if review_mode == "greater":
            args['numReviews'] = {"$gt": int(numReviews[0])}
        elif review_mode == "lesser":
            args['numReviews'] = {"$lt": int(numReviews[0])}
        elif review_mode == "equals":
            if isinstance(numReviews, list) and len(numReviews) > 1:
                args['numReviews'] = {"$in": [int(numReviews) for numReviews in numReviews]}
            elif isinstance(numReviews, list) and len(numReviews) == 1:
                args['numReviews'] = int(numReviews[0])
            else:
                args['numReviews'] = int(numReviews)
    if visitedRestaurants is not None:
        if isinstance(visitedRestaurants, list) and len(visitedRestaurants) > 1:
            args['visitedRestaurants'] = {"$in": [visitedRestaurants for visitedRestaurants in visitedRestaurants]}
        elif isinstance(visitedRestaurants, list) and len(visitedRestaurants) == 1:
            args['visitedRestaurants'] = visitedRestaurants[0]
        else:
            args['visitedRestaurants'] = visitedRestaurants
    return args

def getUser(collection, id=None, username=None, orders_search_mode="equals", numOrders=None, reviews_search_mode = "equals", numReviews=None, visitedRestaurants=None, limit=10, sort="username"):
    """
    Returns a list of users based on the provided parameters.
    """
    if collection is None:
        raise ValueError('Collection is None')
    
    args = queryBuilder(id, username,orders_search_mode, numOrders, reviews_search_mode, numReviews, visitedRestaurants)
  

    cursor = collection.find(args).sort(sort).limit(limit)

    #print(args)
    users = []
    for user in cursor:
        users.append(serialize_document(user))
    return list(users)

def createUser(collection, user):
    """
    Creates a new user in the database.
    """
    if collection is None: 
        raise ValueError('Collection is None')
    user_dict=user.model_dump()
    existing_user = collection.find_one({"id": user_dict["id"]})
    if existing_user:
        raise ValueError('User already exists')
    result = collection.insert_one(user_dict)
    return {"inserted_id": str(result.inserted_id)}

def createMultiplUsers(collection, users):
    """
    Creates multiple users in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    user_dicts = users.model_dump()
    existing_users = collection.find({"id": {"$in": [user["id"] for user in user_dicts]}})
    if existing_users:
        raise ValueError('Some users already exist')
    result = collection.insert_many(user_dicts)
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}

def updateUser(collection, id, user):
    """
    Updates an existing user in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    user_dict = user.model_dump()
    user_dict = {k: v for k, v in user_dict.items() if v is not None}
    result = collection.update_one({"id": int(id)}, {"$set": user_dict})
    if result.matched_count == 0:
        raise ValueError('User not found')
    return {"modified_count": result.modified_count}

def updateMultipleUsers(collection, ids, user):
    """
    Updates multiple users in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    user_dict = user.model_dump()
    user_dict = {k: v for k, v in user_dict.items() if v is not None}
    result = collection.update_many({"id": {"$in": [int(i) for i in ids]}}, {"$set": user_dict})
    return {"modified_count": result.modified_count}

def deleteUser(collection, id):
    """
    Deletes a user from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"id": int(id)})
    return {"deleted_count": result.deleted_count}

def deleteMultipleUsers(collection, ids):
    """
    Deletes multiple users from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"id": {"$in": [int(i) for i in ids]}})
    return {"deleted_count": result.deleted_count}
    
    
def updateUserOrderCount(user_collection, order_collection, user_id: int):
    """
    Updates the number of orders for a given user.
    """
    if user_collection is None or order_collection is None:
        raise ValueError("One or both collections are None")
    
    

    

    order_count = order_collection.count_documents({"userId": int(user_id)})

    result = user_collection.update_one(
        {"id": int(user_id)},
        {"$set": {"numOrders": order_count}}
    )
    return {"user_id": user_id, "numOrders": order_count, "modified_count": result.modified_count}




def updateUserReviewCount(user_collection, review_collection, user_id: int):
    """
    Updates the number of reviews for a given user.
    """
    if user_collection is None or review_collection is None:
        raise ValueError("One or both collections are None")

    review_count = review_collection.count_documents({"userId": int(user_id)})

    result = user_collection.update_one(
        {"id": int(user_id)},
        {"$set": {"numReviews": review_count}}
    )
    return {"user_id": user_id, "numReviews": review_count, "modified_count": result.modified_count}

    