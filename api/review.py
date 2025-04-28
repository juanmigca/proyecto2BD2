import pymongo
from models import Restaurant
from bson import ObjectId
def serialize_document(review):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    review["_id"] = str(review["_id"])
    return review
def queryBuilder(id=None, user_id=None, restaurant_id=None, rating=None):
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
    if rating is not None:
        if isinstance(rating, list) and len(rating) > 1:
            args['rating'] = {"$in": [rating for rating in rating]}
        elif isinstance(rating, list) and len(rating) == 1:
            args['rating'] = rating[0]
        else:
            args['rating'] = rating
    return args