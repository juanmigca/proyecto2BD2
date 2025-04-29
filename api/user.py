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

