import pymongo
from utils.models import Restaurant
from bson import ObjectId
from utils.utilsApi import serialize_document


    
def queryBuilder(id = None, name = None, cuisine = None):
    args = {}
    if id is not None and id!="":
        if isinstance(id, list) and len(id) > 1:
            args['id'] = {"$in": [int(i) for i in id]}
        elif isinstance(id, list) and len(id) == 1:
            args['id'] = int(id[0])
        else:
            args['id'] = int(id)
    if name is not None and name != "":
        if isinstance(name, list) and len(name) > 1:
            args['name'] = {"$in": [n for n in name]}
        elif isinstance(name, list) and len(name) == 1:
            args['name'] = name[0]
        else:
            args['name'] = name
    if cuisine is not None and cuisine != "":
        if isinstance(cuisine, list) and len(cuisine) > 1:
            args['cuisines'] = {"$in": [cuisine for cuisine in cuisine]}
        elif isinstance(cuisine, list) and len(cuisine) == 1:
            args['cuisines'] = cuisine[0]
        else:
            args['cuisines'] = cuisine
    
        
    return args


def getRestaurants(collection, id = None, name = None, cuisine = None, limit = 10, sort = "rating"):
    """
    Returns a list of restaurants.
    """
    
    if collection is None:
        raise ValueError('Collection is None')
    args = queryBuilder(id, name, cuisine)
    #print(args)
    
    cursor = collection.find(args).sort(sort).limit(limit)
    restaurants = []
    for restaurant in cursor:
        restaurants.append(serialize_document(restaurant))

    return list(restaurants)

def createRestaurant(collection, restaurant):
    
    if collection is None:
        raise ValueError('Collection is None')
    
    restaurant_dict = restaurant.model_dump()
    
    existing = collection.find_one({"id": restaurant_dict["id"]})
    if existing:
        raise ValueError('Restaurant with that id already exists')

  
    result = collection.insert_one(restaurant_dict)

    return {"inserted_id": str(result.inserted_id)}
    
def updateRestaurantWrapper(collection, id, name, cuisine, restaurant, mode):
    """
    Updates a restaurant or multiple restaurants.
    """
    
    if mode == "single":
        return updateRestaurant(collection, id, name, cuisine, restaurant)
    elif mode == "multiple":
        return updateMultipleRestaurants(collection, id, name, cuisine, restaurant)

    
    
def updateRestaurant(collection, id, name, cuisine, restaurant):
    """
    Updates a restaurant.
    """

    
    if collection is None:
        raise ValueError('Collection is None')
    
    findquery = queryBuilder(id, name, cuisine)
    
    update_data = {k: v for k, v in restaurant.model_dump().items() if v is not None}

    if not update_data:
        raise ValueError('No data to update')

    result = collection.update_one(
        findquery,           
        {"$set": update_data} 
    )

    return result.modified_count

def updateMultipleRestaurants(collection, id, name, cuisine, restaurants):
    """
    Updates multiple restaurants.
    """
    
    if collection is None:
        raise ValueError('Collection is None')
    
    findQuery = queryBuilder(id, name, cuisine)
    
    update_data = {k: v for k, v in restaurants.dict(exclude_unset=True).items() if v is not None}

    if not update_data:
        raise ValueError("No data to update")

    result = collection.update_many(
        findQuery,           
        {"$set": update_data} 
    )

    return result.modified_count
 



def deleteRestaurant(collection, id, name, cuisines):
    if collection is None:
        raise ValueError('Collection is None')
    
    findquery = queryBuilder(id, name, cuisines)
    
    result = collection.delete_one(findquery)
    
    return result.deleted_count


def deleteMultipleRestaurants(collection, id, name, cuisines):
    if collection is None:
        raise ValueError('Collection is None')
    findquery = queryBuilder(id, name, cuisines)
    
    result = collection.delete_many(findquery)
    
    return result.deleted_count

def deleteRestaurantsWrapper(collection, id, name, cuisines, mode):
    if mode == "single":
        return deleteRestaurant(collection, id, name, cuisines)
    elif mode == "multiple": 
        return deleteMultipleRestaurants(collection, id, name, cuisines)
    else:
        raise ValueError(f"Invalid mode {mode}")
    
def updateRestaurantRating(restaurant_collection, review_collection, restaurant_id: int):
    """
    Updates the average rating and review count for a restaurant.
    """
    if restaurant_collection is None or review_collection is None:
        raise ValueError("One or more collections are None")

    # Obtener todas las reseñas del restaurante
    reviews_cursor = review_collection.find({"restaurantId": int(restaurant_id)})
    reviews = list(reviews_cursor)

    if not reviews:
        # Si no hay reseñas, resetear el rating
        restaurant_collection.update_one(
            {"id": int(restaurant_id)},
            {"$set": {"rating": None, "numReviews": 0}}
        )
        return {"message": "Restaurant rating reset to None"}

    total_stars = sum([r.get("stars", 0) for r in reviews])
    avg_rating = round(total_stars / len(reviews), 2)
    review_count = len(reviews)

    # Actualizar el restaurante
    restaurant_collection.update_one(
        {"id": int(restaurant_id)},
        {"$set": {
            "rating": avg_rating,
            "numReviews": review_count
        }}
    )

    return {"message": f"Restaurant rating updated to {avg_rating} with {review_count} reviews"}
