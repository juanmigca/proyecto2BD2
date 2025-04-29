import pymongo
from models import Review
from bson import ObjectId
def serialize_document(review=Review):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    review["_id"] = str(review["_id"])
    return review
def queryBuilder(id=None, user_id=None, restaurant_id=None, rating=None):
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
    if rating is not None:
        if isinstance(rating, list) and len(rating) > 1:
            args['rating'] = {"$in": [rating for rating in rating]}
        elif isinstance(rating, list) and len(rating) == 1:
            args['rating'] = rating[0]
        else:
            args['rating'] = rating
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

def create_review(collection, review=Review):
    """
    Creates a new review in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    review_dict=review.to_dict()
    existing = collection.find_one({"id": review_dict["id"]})
    if existing:
        raise ValueError('Restaurant with that id already exists')
    result = collection.insert_one(review_dict)
    return {"inserted_id": str(result.inserted_id)}

def update_review(collection, id, review=Review):
    """
    Updates an existing review in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    review_dict = review.to_dict()
    result = collection.update_one({"_id": int(id)}, {"$set": review_dict})
    if result.matched_count == 0:
        raise ValueError(f"No review found with id {id}")
    return {"modified_count": result.modified_count}

def update_multiple_reviews(collection, ids, review=Review):
    """
    Updates multiple reviews in the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    review_dict = review.model_dump()
    result = collection.update_many({"_id": {"$in": [int(i) for i in ids]}}, {"$set": review_dict})
    return {"modified_count": result.modified_count}

def delete_review(collection,id):
    """
    Deletes a review from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_one({"_id": int(id)})
    return {"deleted_count": result.deleted_count}

def delete_multiple_reviews(collection, ids):
    """
    Deletes multiple reviews from the database.
    """
    if collection is None:
        raise ValueError('Collection is None')
    result = collection.delete_many({"_id": {"$in": [int(i) for i in ids]}})
    return {"deleted_count": result.deleted_count}


