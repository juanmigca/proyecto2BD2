from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from utils.utilsApi import getMongoClient, getCollection
from contextlib import asynccontextmanager
from api.helpers.restaurant import getRestaurants, updateRestaurantWrapper, createRestaurant,  deleteRestaurantsWrapper, updateRestaurantRating, updateRestaurantRating2
from api.helpers.menuItems import getMenuItems, createMenuItem, updateMenuItem, deleteMenuItem, deleteMultipleMenuItems, updateMultipleMenuItem
from api.helpers.ingredients import getIngredients, createIngredient, updateIngredient, deleteIngredient, deleteMultipleIngredient, multipleUpdateIngredient
from api.helpers.cuisines import getCuisine, createCuisine, updateCuisine, updateMultipleCuisine, deleteCuisine, deleteMultipleCuisine
from api.helpers.user import getUser, createUser, createMultiplUsers, updateUser, updateMultipleUsers, deleteUser, deleteMultipleUsers, updateUserOrderCount, updateUserReviewCount, updateUserOrderReviewCount, updateUserVisitedRestaurants
from api.helpers.review import getReview, createReview, updateReview, updateMultipleReviews, deleteReview, deleteMultipleReviews
from api.helpers.order import getOrders, createOrder, updateOrder, updateMultipleOrders, deleteOrder, deleteMultipleOrders
from utils.models import Restaurant, User, Review, Order, MenuItem, Ingredient, Cuisines
from api.helpers.formularios import get_formulario


### Defaults
default_restaurant = Restaurant(
    id =None,
    name=None,
    address=None,
    cuisines = None,
    location = None,
    menuItems = None,
    rating = None,
    numReviews = None)


### DB 

mongo_client = None

db = 'proyecto2bd'


@asynccontextmanager
async def lifespan(app: FastAPI):
    global mongo_client
    mongo_client = getMongoClient()
    print("Connected to MongoDB!")

    yield

    mongo_client.close()
    print("Closed connection to MongoDB.")

    
### Startup
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[""]
)

### API Management

@app.get("/favicon.ico")
async def favicon():
    return {'status': 204}

@app.get("/root")
def read_root():
    return {'Status': 'Activo.'}

### Restaurants

@app.get("/restaurants")
def get_restaurants(id: Union[str, list, None] = Query(default=None), name: Union[str, list, None] = Query(default=None), cuisine: Union[str, list, None] = Query(default=None), limit: int = Query(default=10), sort: str = Query(default="rating")):
    """
    Returns a list of restaurants.
    """
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    
    try:
        #print(id, name, cuisine)
        restaurants = getRestaurants(restaurant_collection, id, name, cuisine, limit)
    except:
        return {'status': 500,
                'message': 'Query execution error'}
    return {'status': 200, 
            'data': restaurants}



@app.patch("/restaurants")
def update_restaurant(find_id: Union[str, None] = Query(default=None), find_name: Union[str,None] = Query(default=None), find_cuisine: Union[str, list, None]= Query(default=None), restaurant: Restaurant = default_restaurant):
    
    
    """
    Updates a restaurant.
    """
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    try:
        res = updateRestaurantWrapper(restaurant_collection, find_id, find_name, find_cuisine, restaurant, "single")
    except ValueError as e:
        return {'status': 500,
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error updating restaurant'}
    
    return {'status': 200, 
            'message': f'Restaurant updated'}




@app.patch("/batch/restaurants")
def update_multiple_restaurants(find_id: Union[list, str, None] = Query(default=None), find_name: Union[list, str, None] = Query(default=None), find_cuisine: Union[list, str, None] = Query(default=None), restaurant: Restaurant = default_restaurant):
    """
    Updates multiple restaurants.
    """
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        res = updateRestaurantWrapper(restaurant_collection, find_id, find_name, find_cuisine, restaurant, "multiple")
    except ValueError as e:
        return {'status': 500, 
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error updating restaurant'}
    
    return {'status': 200, 
            'message': f'{res} restaurants updated'}
    

@app.post("/restaurants")
def create_restaurant(restaurant: Restaurant):
    """
    Creates a restaurant
    """

    restaurant_collection = getCollection(mongo_client, db, 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    try:
        createRestaurant(restaurant_collection, restaurant)
    except ValueError as e:
        
        return {'status': 500, 
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error creating restaurant'}
        
    return {'status': 200, 
            'message': f'Restaurant created'}

@app.delete("/restaurants")
def delete_restaurant(find_id: Union[str, None] = Query(default=None), find_name: Union[str, None] = Query(default=None), find_cuisine: Union[list, str, None] = Query(default=None)):
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    try:
        deleteRestaurantsWrapper(restaurant_collection, find_id, find_name, find_cuisine, "single")
    except ValueError as e:
        
        return {'status': 500, 
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error deleting restaurant'}
        
    return {'status': 200, 
            'message': f'Restaurant deleted'}

@app.delete("/batch/restaurants")
def delete_multiple_restaurants(find_id: Union[list, str, None] = Query(default=None), find_name: Union[list, str, None] = Query(default=None), find_cuisine: Union[list, str, None] = Query(default=None)):
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    try:
        deleteRestaurantsWrapper(restaurant_collection, find_id, find_name, find_cuisine, "multiple")
    except ValueError as e:
        
        return {'status': 500, 
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error deleting restaurants'}
        
    return {'status': 200, 
            'message': f'Restaurans deleted'}

### Cuisines

@app.get("/cuisines")
def get_cuisines(id: Union[str, list, None] = Query(default=None), name: Union[str, list, None] = Query(default=None), limit: Union[int, None] = Query(default=None), sort: str = Query(default="name")):
    """
    Returns a list of cuisines.
    """
    cuisine_collection = getCollection(mongo_client, db, 'cuisines')
    if cuisine_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        cuisines = getCuisine(cuisine_collection, id, name, limit, sort)
    except:
        return {'status': 500,
                'message': 'Query execution error'}
    return {'status': 200, 
            'data': cuisines}

@app.post("/cuisines")
def create_cuisine(cuisine: Cuisines):
    """
    Creates a cuisine.
    """
    collection = getCollection(mongo_client, db, 'cuisines')
    return {'status': 200, 'data': createCuisine(collection, cuisine)}

@app.patch("/cuisines")
def update_cuisine(id: str, cuisine: Cuisines):
    """
    Updates a cuisine.
    """
    collection = getCollection(mongo_client, db, 'cuisines')
    return {'status': 200, 'data': updateCuisine(collection, id, cuisine)}

@app.delete("/cuisines")
def delete_cuisine(id: str):
    """
    Deletes a cuisine.
    """
    collection = getCollection(mongo_client, db, 'cuisines')
    return {'status': 200, 'data': deleteCuisine(collection, id)}

@app.patch("/batch/cuisines")
def update_multiple_cuisines(ids: list[str], cuisine: Cuisines):
    collection = getCollection(mongo_client, db, 'cuisines')
    return {'status': 200, 'data': updateMultipleCuisine(collection, ids, cuisine)}

@app.delete("/batch/cuisines")
def delete_multiple_cuisines(ids: list[str]):
    collection = getCollection(mongo_client, db, 'cuisines')
    return {'status': 200, 'data': deleteMultipleCuisine(collection, ids)}


### Menu Items

@app.get("/menuItems")
def get_menuItems(id: Union[str, list, None] = Query(default=None), name: Union[str, list, None] = Query(default=None), limit: Union[int, None] = Query(default=None), sort: str = Query(default="addedToMenu")):
    """
    Returns a list of menu items.
    """
    menuItem_collection = getCollection(mongo_client, db, 'menuItems')
    if menuItem_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        menuItems = getMenuItems(menuItem_collection, id, name, limit, sort)
    except:
        return {'status': 500,
                'message': 'Query execution error'}
    return {'status': 200, 
            'data': menuItems}



@app.post("/menuItems")
def create_menu_item(menu_item: MenuItem):
    """
    Creates a menu item.
    """
    menuItem_collection = getCollection(mongo_client, db, 'menuItems')
    if menuItem_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        createMenuItem(menuItem_collection, menu_item)
    except ValueError as e:
        
        return {'status': 500, 
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error creating menu item'}
        
    return {'status': 200, 
            'message': f'Menu item created'}

@app.patch("/menuItems")
def update_menu_item(find_id: Union[str, None] = Query(default=None), menu_item: MenuItem = MenuItem):
    """
    Updates a menu item.
    """
    menuItem_collection = getCollection(mongo_client, db, 'menuItems')
    if menuItem_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        updateMenuItem(menuItem_collection, find_id, menu_item)
    except ValueError as e:
        
        return {'status': 500, 
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error updating menu item'}
        
    return {'status': 200, 
            'message': f'Menu item updated'}

@app.patch("/batch/menuItems")
def update_multiple_menu_items(find_id: Union[list, str, None] = Query(default=None), menu_item: MenuItem = MenuItem):
    """
    Updates multiple menu items.
    """
    menuItem_collection = getCollection(mongo_client, db, 'menuItems')
    if menuItem_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        updateMultipleMenuItem(menuItem_collection, find_id, menu_item)
    except ValueError as e:
        
        return {'status': 500, 
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error updating menu items'}
        
    return {'status': 200, 
            'message': f'Menu items updated'}

@app.delete("/menuItems")
def delete_menu_item(find_id: Union[str, None] = Query(default=None)):
    """
    Deletes a menu item.
    """
    menuItem_collection = getCollection(mongo_client, db, 'menuItems')
    if menuItem_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        deleteMenuItem(menuItem_collection, find_id)
    except ValueError as e:
        
        return {'status': 500, 
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error deleting menu item'}
        
    return {'status': 200, 
            'message': f'Menu item deleted'}

@app.delete("/batch/menuItems")
def delete_multiple_menu_items(find_id: Union[list, str, None] = Query(default=None)):
    """
    Deletes multiple menu items.
    """
    menuItem_collection = getCollection(mongo_client, db, 'menuItems')
    if menuItem_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        deleteMultipleMenuItems(menuItem_collection, find_id)
    except ValueError as e:
        
        return {'status': 500, 
                'message': e}
    except:
        return {'status': 500,
                'message': 'Error deleting menu items'}
        
    return {'status': 200, 
            'message': f'Menu items deleted'}


### Ingredients

@app.get("/ingredients")
def get_ingredients(name: Union[str, list, None] = Query(default=None), amount: Union[str, list, None] = Query(default=None), unitMeasure: Union[str, list, None] = Query(default=None), limit: Union[int, None] = Query(default=None), sort: str = Query(default="name")):
    """
    Returns a list of ingredients.
    """
    ingredient_collection = getCollection(mongo_client, db, 'ingredients')
    if ingredient_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        print(name, amount, unitMeasure, limit, sort)
        ingredients = getIngredients(ingredient_collection, name, amount, unitMeasure, limit, sort)
    except:
        return {'status': 500,
                'message': 'Query execution error'}
    return {'status': 200, 
            'data': ingredients}




### Users


@app.get("/users")
def get_users(id: Union[str, list, None] = Query(default=None), 
              username: Union[str, list, None] = Query(default=None), 
              orderMode: Union[str, None] = Query(default="equals"),
              numOrders: Union[int, list, None] = Query(default=None),
              reviewsMode: Union[str,None] = Query(default="equals"),
              numReviews: Union[int, list, None] = Query(default=None), 
              visitedRestaurants: Union[str, list, None] = Query(default=None), 
              limit: Union[int, None] = Query(default=10),
              sort: str = Query(default="username")):
    """
    Returns a list of users.
    """
    user_collection = getCollection(mongo_client, db, 'users')
    if user_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}

    try:
        if id is None:
            updateUserVisitedRestaurants(user_collection,id)
        users = getUser(user_collection, id, username, orderMode, numOrders, reviewsMode, numReviews, visitedRestaurants, limit, sort)
    except:
        return {'status': 500, 'message': 'Query execution error'}
    return {'status': 200, 'data': users}

@app.post("/users")
def create_user(user: User):
    """
    Creates a user.
    """
    user_collection = getCollection(mongo_client, db, 'users')
    if user_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        createUser(user_collection, user)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error creating user'}

    return {'status': 200, 'message': 'User created'}

@app.patch("/users")
def update_user(find_id: Union[str, None] = Query(default=None), user: User = User):
    """
    Updates a user.
    """
    user_collection = getCollection(mongo_client, db, 'users')
    if user_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}

    try:
        updateUser(user_collection, find_id, user)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error updating user'}

    return {'status': 200, 'message': 'User updated'}

@app.patch("/batch/users")
def update_multiple_users(find_id: Union[list, str, None] = Query(default=None), user: User = User):
    """
    Updates multiple users.
    """
    user_collection = getCollection(mongo_client, db, 'users')
    if user_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}

    try:
        ids = find_id if isinstance(find_id, list) else [find_id]
        updateMultipleUsers(user_collection, ids, user)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error updating users'}

    return {'status': 200, 'message': 'Users updated'}

@app.delete("/users")
def delete_user(find_id: Union[str, None] = Query(default=None)):
    """
    Deletes a user.
    """
    user_collection = getCollection(mongo_client, db, 'users')
    if user_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}

    try:
        deleteUser(user_collection, find_id)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error deleting user'}

    return {'status': 200, 'message': 'User deleted'}

@app.delete("/batch/users")
def delete_multiple_users(find_id: Union[list, str, None] = Query(default=None)):
    """
    Deletes multiple users.
    """
    user_collection = getCollection(mongo_client, db, 'users')
    if user_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}

    try:
        ids = find_id if isinstance(find_id, list) else [find_id]
        deleteMultipleUsers(user_collection, ids)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error deleting users'}

    return {'status': 200, 'message': 'Users deleted'}

### Orders

@app.post("/orders")
def create_order(order: Order):
    """
    Creates a new order and updates the user's order count.
    """
    order_collection = getCollection(mongo_client, db, 'orders')
    user_collection = getCollection(mongo_client, db, 'users')

    if order_collection is None or user_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}

    try:
        createOrder(order_collection, order)
        #updateUserOrderCount(user_collection, order_collection, user_id=order.userId)
        updateUserOrderReviewCount(user_collection, order.userId)
        updateUserVisitedRestaurants(user_collection,order.userId)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except Exception as e:
        return {'status': 500, 'message': f'Error creating order: {e}'}

    return {'status': 200, 'message': 'Order created and user order count updated'}


@app.delete("/orders")
def delete_order(find_id: Union[str, None] = Query(default=None)):
    """
    Deletes a single order and updates the user's order count.
    """
    order_collection = getCollection(mongo_client, db, 'orders')
    user_collection = getCollection(mongo_client, db, 'users')
    review_collection = getCollection(mongo_client, db, 'reviews')

    if order_collection is None or user_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}

    try:
        # Buscar la orden primero para obtener userId
        order_doc = order_collection.find_one({"id": int(find_id)})
        if not order_doc:
            raise ValueError("Order not found")

        user_id = order_doc.get("userId")
        deleteOrder(order_collection, find_id)
        #updateUserOrderCount(user_collection, order_collection, user_id=user_id)
        updateUserOrderReviewCount(user_collection, user_id)
        deleteMultipleReviews(review_collection, order=find_id)
        updateUserVisitedRestaurants(user_collection,user_id)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except Exception as e:
        return {'status': 500, 'message': f'Error deleting order: {e}'}

    return {'status': 200, 'message': 'Order deleted and user order count updated'}


@app.delete("/batch/orders")
def delete_multiple_orders(find_id: Union[int, list, None]= Query(default=None)):
    """
    Deletes multiple orders.
    """
    order_collection = getCollection(mongo_client, db, 'orders')
    user_collection = getCollection(mongo_client, db, 'users')
    review_collection = getCollection(mongo_client, db, 'reviews')
    if order_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    user_ids = []
    try:
        print(find_id)
        for order_id in find_id:
            order_doc = order_collection.find_one({"id": int(order_id)})
            print(order_doc)
            if order_doc:
                user_ids.append(order_doc.get("userId"))
                deleteMultipleReviews(review_collection, order=order_id)
        deleteMultipleOrders(order_collection, find_id)
        for user_id in user_ids:
            #updateUserOrderCount(user_collection, order_collection, user_id=user_id)
            updateUserOrderReviewCount(user_collection, user_id)
            updateUserVisitedRestaurants(user_collection,user_id)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error deleting orders'}
    return {'status': 200, 'message': 'Orders deleted'}

@app.patch("/orders")
def update_order(find_id: Union[str, None] = Query(default=None), order: Order = Order):
    """
    Updates a single order.
    """
    order_collection = getCollection(mongo_client, db, 'orders')
    if order_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        updateOrder(order_collection, find_id, order)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error updating order'}
    return {'status': 200, 'message': 'Order updated'}

@app.patch("/batch/orders")
def update_multiple_orders(find_id: Union[str, list, None] = Query(default=None), order: Order = Order):
    """
    Updates multiple orders.
    """
    order_collection = getCollection(mongo_client, db, 'orders')
    if order_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        updateMultipleOrders(order_collection, find_id, order)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error updating orders'}
    return {'status': 200, 'message': 'Orders updated'}

@app.get("/orders")
def get_orders(
    id: Union[str, list, None] = Query(default=None),
    user_id: Union[str, list, None] = Query(default=None),
    restaurant_id: Union[str, list, None] = Query(default=None),
    status: Union[str, list, None] = Query(default=None),
    limit: int = Query(default=10),
    sort: str = Query(default="orderedAt")):
    """
    Returns a list of orders.
    """
    order_collection = getCollection(mongo_client, db, 'orders')
    if order_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        orders = getOrders(order_collection, id, user_id, restaurant_id, status, limit, sort)
    except:
        return {'status': 500, 'message': 'Query execution error'}
    return {'status': 200, 'data': orders}

### 


@app.get("/reviews")
def get_reviews(
    id: Union[str, list, None] = Query(default=None),
    user_id: Union[str, list, None] = Query(default=None),
    order_id: Union[str, list, None] = Query(default=None),
    restaurant_id: Union[str, list, None] = Query(default=None),
    rating: Union[str, list, None] = Query(default=None),
    limit: int = Query(default=10)
):
    collection = getCollection(mongo_client, db, 'reviews')
    if collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        reviews = getReview(collection, id, user_id, order_id, restaurant_id, rating, limit)
    except:
        return {'status': 500, 'message': 'Query execution error'}
    return {'status': 200, 'data': reviews}

@app.post("/reviews")
def create_review(review: Review):
    collection = getCollection(mongo_client, db, 'reviews')
    user_collection = getCollection(mongo_client, db, 'users')
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')

    if collection is None or user_collection is None or restaurant_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        createReview(collection, review)
        #updateUserReviewCount(user_collection, collection, user_id=review.userId)
        updateUserOrderReviewCount(user_collection, review.userId)
        updateRestaurantRating2(restaurant_collection, restaurant_id=review.restaurantId)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except Exception as e:
        return {'status': 500, 'message': f'Error creating review: {e}'}

    return {'status': 200, 'message': 'Review created and counts updated'}

@app.patch("/reviews")
def update_review(find_id: Union[str, None] = Query(default=None), review: Review = Review):
    collection = getCollection(mongo_client, db, 'reviews')
    user_collection = getCollection(mongo_client, db, 'users')
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')

    if collection is None or user_collection is None or restaurant_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        updateReview(collection, find_id, review)
        review_doc = collection.find_one({"id": int(find_id)})
        if review_doc:
            #updateUserReviewCount(user_collection, collection, user_id=review_doc['userId'])
            updateUserOrderReviewCount(user_collection, review_doc['userId'])
            updateRestaurantRating2(restaurant_collection, restaurant_id=review_doc['restaurantId'])
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except Exception as e:
        return {'status': 500, 'message': f'Error updating review: {e}'}
    return {'status': 200, 'message': 'Review updated and counts refreshed'}

@app.patch("/batch/reviews")
def update_multiple_reviews(find_id: Union[list, str, None] = Query(default=None), review: Review = Review):
    collection = getCollection(mongo_client, db, 'reviews')
    user_collection = getCollection(mongo_client, db, 'users')
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')

    if collection is None or user_collection is None or restaurant_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}

    try:
        updateMultipleReviews(collection, find_id, review)
        ids = find_id if isinstance(find_id, list) else [find_id]
        for review_id in ids:
            review_doc = collection.find_one({"id": int(review_id)})
            if review_doc:
                #updateUserReviewCount(user_collection, collection, user_id=review_doc['userId'])
                updateUserOrderReviewCount(user_collection, review_doc['userId'])
                updateRestaurantRating2(restaurant_collection, restaurant_id=review_doc['restaurantId'])
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except Exception as e:
        return {'status': 500, 'message': f'Error updating reviews: {e}'}
    return {'status': 200, 'message': 'Reviews updated and counts refreshed'}

@app.delete("/reviews")
def delete_review(find_id: Union[str, None] = Query(default=None)):
    collection = getCollection(mongo_client, db, 'reviews')
    user_collection = getCollection(mongo_client, db, 'users')
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')

    if collection is None or user_collection is None or restaurant_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        review_doc = collection.find_one({"id": int(find_id)})
        if not review_doc:
            raise ValueError("Review not found")
        deleteReview(collection, find_id)
        #updateUserReviewCount(user_collection, collection, user_id=review_doc['userId'])
        updateUserOrderReviewCount(user_collection, review_doc['userId'])
        updateRestaurantRating2(restaurant_collection, restaurant_id=review_doc['restaurantId'])
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except Exception as e:
        return {'status': 500, 'message': f'Error deleting review: {e}'}

    return {'status': 200, 'message': 'Review deleted and counts updated'}

@app.delete("/batch/reviews")
def delete_multiple_reviews(find_id: Union[list, str, None] = Query(default=None)):
    collection = getCollection(mongo_client, db, 'reviews')
    user_collection = getCollection(mongo_client, db, 'users')
    restaurant_collection = getCollection(mongo_client, db, 'restaurants')

    if collection is None or user_collection is None or restaurant_collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}

    try:
        ids = find_id if isinstance(find_id, list) else [find_id]
        for rid in ids:
            review_doc = collection.find_one({"id": int(rid)})
            if review_doc:
                deleteReview(collection, rid)
                #updateUserReviewCount(user_collection, collection, user_id=review_doc['userId'])
                updateUserOrderReviewCount(user_collection, review_doc['userId'])
                updateRestaurantRating2(restaurant_collection, restaurant_id=review_doc['restaurantId'])
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except Exception as e:
        return {'status': 500, 'message': f'Error deleting reviews: {e}'}

    return {'status': 200, 'message': 'Reviews deleted and counts updated'}

### Formularios de Resúmenes
@app.get("/summary")
def get_summary(tipo: str):
    """
    Returns the requested summary.
    """
    collection = getCollection(mongo_client, db, 'Resumenes')
    if tipo == 'Resumen Ingredientes':
        collection2 = getCollection(mongo_client, db, 'ingredients')
    elif tipo == 'Resumen Cuisines':
        collection2 = getCollection(mongo_client, db, 'cuisines')
    elif tipo == 'Resumen Menu Items':
        collection2 = getCollection(mongo_client, db, 'menuItems')
    elif tipo == 'Resumen Órdenes por Status' or tipo == 'Resumen Órdenes':
        collection2 = getCollection(mongo_client, db, 'orders')
    elif tipo == 'Resumen Restaurantes':
        collection2 = getCollection(mongo_client, db, 'restaurants')
    elif tipo == 'Resumen Reviews':
        collection2 = getCollection(mongo_client, db, 'reviews')
    elif tipo == 'Resumen Por Usuario' or tipo == 'Resumen Usuario Promedio':
        collection2 = getCollection(mongo_client, db, 'users')
    
    if collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        content = get_formulario(collection,collection2,  tipo)
        if content is None:
            return {'status': 404, 'message': 'Summary not found'}
    except:
        return {'status': 500, 'message': 'Query execution error'}
    return {'status': 200, 'data': content}

### Ingredients

@app.post("/ingredients")
def create_ingredient(ingredient: Ingredient):
    """
    Creates an ingredient.
    """
    collection = getCollection(mongo_client, db, 'ingredients')
    if collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        createIngredient(collection, ingredient)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error creating ingredient'}
    return {'status': 200, 'message': 'Ingredient created'}

@app.patch("/ingredients")
def update_ingredient(find_name: Union[str, None] = Query(default=None), ingredient: Ingredient = Ingredient):
    """
    Updates an ingredient.
    """
    collection = getCollection(mongo_client, db, 'ingredients')
    if collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        updateIngredient(collection, find_name, ingredient)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error updating ingredient'}
    return {'status': 200, 'message': 'Ingredient updated'}

@app.patch("/batch/ingredients")
def update_multiple_ingredients(find_name:Union[list, str, None] = Query(default=None), ingredient: Ingredient = Ingredient):
    """
    Updates multiple ingredients.
    """
    collection = getCollection(mongo_client, db, 'ingredients')
    if collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        multipleUpdateIngredient(collection, names, ingredient)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error updating ingredients'}
    return {'status': 200, 'message': 'Ingredients updated'}

@app.delete("/ingredients")
def delete_ingredient(find_name: Union[str,None] = Query(default=None)):
    """
    Deletes a single ingredient.
    """
    collection = getCollection(mongo_client, db, 'ingredients')
    if collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        deleteIngredient(collection, find_name)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error deleting ingredient'}
    return {'status': 200, 'message': 'Ingredient deleted'}

@app.delete("/batch/ingredients")
def delete_multiple_ingredients(find_name: Union[str, list, None] = Query(default=None)):
    """
    Deletes multiple ingredients.
    """
    collection = getCollection(mongo_client, db, 'ingredients')
    if collection is None:
        return {'status': 502, 'message': 'Error connecting to collection'}
    try:
        deleteMultipleIngredient(collection, find_name)
    except ValueError as e:
        return {'status': 500, 'message': str(e)}
    except:
        return {'status': 500, 'message': 'Error deleting ingredients'}
    return {'status': 200, 'message': 'Ingredients deleted'}