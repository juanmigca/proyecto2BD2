from models import User
from bson import ObjectId

def serialize_document(user=User):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    user["_id"] = str(user["_id"])
    return user

def queryBuilder(id=None, username=None, numReviews=None, visitedRestaurants=None):
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
    if username is not None:
        if isinstance(username, list) and len(username) > 1:
            args['username'] = {"$in": [username for username in username]}
        elif isinstance(username, list) and len(username) == 1:
            args['username'] = username[0]
        else:
            args['username'] = username
    if numReviews is not None:
        if isinstance(numReviews, list) and len(numReviews) > 1:
            args['numReviews'] = {"$in": [numReviews for numReviews in numReviews]}
        elif isinstance(numReviews, list) and len(numReviews) == 1:
            args['numReviews'] = numReviews[0]
        else:
            args['numReviews'] = numReviews
    if visitedRestaurants is not None:
        if isinstance(visitedRestaurants, list) and len(visitedRestaurants) > 1:
            args['visitedRestaurants'] = {"$in": [visitedRestaurants for visitedRestaurants in visitedRestaurants]}
        elif isinstance(visitedRestaurants, list) and len(visitedRestaurants) == 1:
            args['visitedRestaurants'] = visitedRestaurants[0]
        else:
            args['visitedRestaurants'] = visitedRestaurants
    return args

def get_user(collection, id=None, username=None, numReviews=None, visitedRestaurants=None, limit=10):
    """
    Returns a list of users based on the provided parameters.
    """
    if collection is None:
        raise ValueError('Collection is None')
    args = queryBuilder(id, username, numReviews, visitedRestaurants)
    cursor = collection.find(args).limit(limit)
    users = []
    for user in cursor:
        users.append(serialize_document(user))
    return list(users)

def create_user(collection, user=User):
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

def create_multiple_users(collection, users):
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

def update_user(collection, id, user=User):
    """
    Updates an existing user in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    user_dict = user.model_dump()
    result = collection.update_one({"_id": int(id)}, {"$set": user_dict})
    if result.matched_count == 0:
        raise ValueError('User not found')
    return {"modified_count": result.modified_count}

def update_multiple_users(collection, ids, user=User):
    """
    Updates multiple users in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    user_dict = user.model_dump()
    result = collection.update_many({"_id": {"$in": [int(i) for i in ids]}}, {"$set": user_dict})
    return {"modified_count": result.modified_count}

def delete_user(collection, id):
    """
    Deletes a user from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"_id": int(id)})
    return {"deleted_count": result.deleted_count}

def delete_multiple_users(collection, ids):
    """
    Deletes multiple users from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"_id": {"$in": [int(i) for i in ids]}})
    return {"deleted_count": result.deleted_count}
    
    
    