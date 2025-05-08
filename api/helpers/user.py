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
    new_id = collection.find_one({}, sort=[("id", -1)]).get("id", 0) + 1
    user_dict["id"] = new_id
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

def updateUserOrderReviewCount(user_collection, user_id: int):
    """
    Updates the number of orders and reviews for a given user.
    """
    if user_collection is None:
        raise ValueError("Collection is None")
    before_update = user_collection.find_one({"id": user_id})
    if before_update is None:
        raise ValueError("User not found")
    before_order_count = before_update.get("numOrders", 0)
    before_review_count = before_update.get("numReviews", 0)
    
    pipeline = [
        {
            '$match': {
                'id': user_id
            }
        }, {
            '$lookup': {
                'from': 'orders', 
                'localField': 'id', 
                'foreignField': 'userId', 
                'as': 'orders'
            }
        }, {
            '$lookup': {
                'from': 'reviews', 
                'localField': 'id', 
                'foreignField': 'userId', 
                'as': 'reviews'
            }
        }, {
            '$addFields': {
                'numOrders': {
                    '$size': '$orders'
                }, 
                'numReviews': {
                    '$size': '$reviews'
                }
            }
        }, {
            '$project': {
                'orders': 0, 
                'reviews': 0
            }
        }, {
            '$merge': {
                'into': 'users', 
                'on': '_id', 
                'whenMatched': 'merge', 
                'whenNotMatched': 'discard'
            }
        }
    ]
    user_collection.aggregate(pipeline)
    updated_user = user_collection.find_one({"id": user_id})
    if updated_user is None:
        raise ValueError("User not found after update")
    after_order_count = updated_user.get("numOrders", 0)
    after_review_count = updated_user.get("numReviews", 0)
    return {
        "user_id": user_id, 
        "numOrders": {
            "before": before_order_count, 
            "after": after_order_count
        }, 
        "numReviews": {
            "before": before_review_count, 
            "after": after_review_count
        }
    }

def updateUserVisitedRestaurants(user_collection, user_id: int):
    if user_collection is None:
        raise ValueError("Collection is None")
    before_update = user_collection.find_one({"id": user_id})
    if before_update is None:
        raise ValueError("User not found")
    before_visited_restaurants = before_update.get("visitedRestaurants", [])
    pipeline = [
        {
            '$match': {
                'id': user_id
            }
        }, {
            '$lookup': {
                'from': 'orders', 
                'localField': 'id', 
                'foreignField': 'userId', 
                'as': 'orders'
            }
        }, {
            '$project': {
                'id': 1, 
                'username': 1, 
                'numOrders': 1, 
                'numReviews': 1, 
                'visitedRestaurants': 1, 
                'orders': {
                    '$filter': {
                        'input': '$orders', 
                        'as': 'order', 
                        'cond': {
                            '$eq': [
                                '$$order.status', 'Entregado'
                            ]
                        }
                    }
                }
            }
        }, {
            '$addFields': {
                'visitedRestaurants': {
                    '$setUnion': [
                        [], {
                            '$map': {
                                'input': '$orders', 
                                'as': 'order', 
                                'in': '$$order.restaurantId'
                            }
                        }
                    ]
                }
            }
        }, {
            '$project': {
                'orders': 0
            }
        }
    ]
    result = user_collection.aggregate(pipeline)
    for cursor in result:
        after_visited_restaurants = cursor.get("visitedRestaurants", [])
    
    set_before = set(before_visited_restaurants)
    set_after = set(after_visited_restaurants)
    new_restaurants = list(set_after - set_before)
    deleted_restaurants = list(set_before - set_after)

    #add new restaurants
    if new_restaurants:
        user_collection.update_one(
            {"id": user_id},
            {"$addToSet": {"visitedRestaurants": {"$each": new_restaurants}}}
        )

    #remove deleted restaurants
    if deleted_restaurants:
        user_collection.update_one(
            {"id": user_id},
            {"$pull": {"visitedRestaurants": {"$in": deleted_restaurants}}}
        )
    return {"user_id": user_id, "visitedRestaurants": after_visited_restaurants}
