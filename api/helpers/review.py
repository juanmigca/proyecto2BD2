import pymongo
from utils.models import Review
from bson import ObjectId
from utils.utilsApi import serialize_document

def queryBuilder(id=None, user_id=None, order_id=None, restaurant_id=None, rating=None):
    args = {}
    if id is not None:
        if isinstance(id, list) and len(id) > 1:
            args['id'] = {"$in": [int(i) for i in id]}
        elif isinstance(id, list) and len(id) == 1:
            args['id'] = int(id[0])
        else:
            args['id'] = int(id)
    if user_id is not None:
        if isinstance(user_id, list) and len(user_id) > 1:
            args['userId'] = {"$in": [int(user_id) for user_id in user_id]}
        elif isinstance(user_id, list) and len(user_id) == 1:
            args['userId'] = int(user_id[0])
        else:
            args['userId'] = int(user_id)
    if order_id is not None:
        if isinstance(order_id, list) and len(order_id) > 1:
            args['orderId'] = {"$in": [int(order_id) for order_id in order_id]}
        elif isinstance(order_id, list) and len(order_id) == 1:
            args['orderId'] = int(order_id[0])
        else:
            args['orderId'] = int(order_id)
    if restaurant_id is not None:
        if isinstance(restaurant_id, list) and len(restaurant_id) > 1:
            args['restaurantId'] = {"$in": [int(restaurant_id) for restaurant_id in restaurant_id]}
        elif isinstance(restaurant_id, list) and len(restaurant_id) == 1:
            args['restaurantId'] = int(restaurant_id[0])
        else:
            args['restaurantId'] = int(restaurant_id)
    if rating is not None:
        if isinstance(rating, list) and len(rating) > 1:
            args['stars'] = {"$in": [rating for rating in rating]}
        elif isinstance(rating, list) and len(rating) == 1:
            args['stars'] = rating[0]
        else:
            args['stars'] = rating
    return args

def get_review(collection, id=None, user_id=None, restaurant_id=None, rating=None, limit=10):
    """
    Returns a list of reviews.
    """
    if collection is None:
        raise ValueError('Collection is None')
    args = queryBuilder(id, user_id, restaurant_id, rating)
    cursor = collection.find(args).limit(limit)
    reviews = []
    for review in cursor:
        reviews.append(serialize_document(review))
    return list(reviews)

def createReview(collection, review):
    """
    Creates a new review in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    review_dict=review.model_dump()
    
    new_id = collection.find_one({}, sort=[("id", -1)]).get("id", 0) + 1    
    review_dict["id"] = new_id

    
    result = collection.insert_one(review_dict)
    return {"inserted_id": str(result.inserted_id)}

def updateReview(collection, id, review):
    """
    Updates an existing review in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    review_dict = review.model_dump()
    review_dict = {k: v for k, v in review_dict.items() if v is not None}
    result = collection.update_one({"id": int(id)}, {"$set": review_dict})
    if result.matched_count == 0:
        raise ValueError(f"No review found with id {id}")
    return {"modified_count": result.modified_count}

def updateMultipleReviews(collection, ids, review):
    """
    Updates multiple reviews in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    review_dict = review.model_dump()
    review_dict = {k: v for k, v in review_dict.items() if v is not None}
    result = collection.update_many({"id": {"$in": [int(i) for i in ids]}}, {"$set": review_dict})
    return {"modified_count": result.modified_count}

def deleteReview(collection,id):
    """
    Deletes a review from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"id": int(id)})
    return {"deleted_count": result.deleted_count}

def deleteMultipleReviews(collection, ids=None, order=None, restaurant=None):
    """
    Deletes multiple reviews from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    query = queryBuilder(id=ids, order_id=order, restaurant_id=restaurant)
    result = collection.delete_many(query)
    return {"deleted_count": result.deleted_count}



