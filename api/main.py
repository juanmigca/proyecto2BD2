from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from utilsApi import getMongoClient, getCollection
from contextlib import asynccontextmanager
from restaurant import getRestaurants, updateRestaurant, createRestaurant, getCuisines
from menuItems import getMenuItems
from models import Restaurant, User, Review, Order, MenuItem


### DB 

mongo_client = None

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
    restaurant_collection = getCollection(mongo_client, 'proyecto2bd', 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    
    try:
        print(id, name, cuisine)
        restaurants = getRestaurants(restaurant_collection, id, name, cuisine, limit)
    except:
        return {'status': 500,
                'message': 'Query execution error'}
    return {'status': 200, 
            'data': restaurants}



@app.patch("/restaurants/{restaurant_id}")
def update_restaurant(restaurant_id: str, restaurant: Restaurant):
    
    
    """
    Updates a restaurant.
    """
    restaurant_collection = getCollection(mongo_client, 'proyecto2bd', 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    try:
        updateRestaurant(restaurant_collection, {restaurant_id}, restaurant)
    except:
        return {'status': 500,
                'message': 'Error updating restaurant'}
    return {'status': 200, 
            'message': f'Restaurant with id {restaurant_id} updated'}


    
@app.post("/restaurants")
def create_restaurant(restaurant: Restaurant):
    """
    Creates a restaurant
    """

    restaurant_collection = getCollection(mongo_client, 'proyecto2db', 'restaurants')
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
    
### Cuisines

@app.get("/cuisines")
def get_cuisines():
    """
    Returns a list of cuisines.
    """
    cuisine_collection = getCollection(mongo_client, 'proyecto2bd', 'cuisines')
    if cuisine_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        cuisines = getCuisines(cuisine_collection)
    except:
        return {'status': 500,
                'message': 'Query execution error'}
    return {'status': 200, 
            'data': cuisines}


@app.patch("/batch/restaurants")
def update_multiple_restaurants(ids: Union[list, None], restaurant: Restaurant):
    """
    Updates multiple restaurants.
    """
    restaurant_collection = getCollection(mongo_client, 'proyecto2bd', 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        updateRestaurant(restaurant_collection, ids, restaurant)
    except:
        return {'status': 500,
                'message': 'Error updating restaurant'}
    return {'status': 200, 
            'message': f'Restaurants with ids {ids} updated'}
    

### Menu Items

@app.get("/menuItems")
def get_menuItems(id: Union[str, list, None] = Query(default=None), ingredient: Union[str, list, None] = Query(default=None), restaurant: Union[str, list, None] = Query(default=None), limit: int = Query(default=None)):
    """
    Returns a list of menu items.
    """
    menuItem_collection = getCollection(mongo_client, 'proyecto2bd', 'menuItems')
    if menuItem_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    try:
        menuItems = getMenuItems(menuItem_collection, id, ingredient, restaurant, limit)
    except:
        return {'status': 500,
                'message': 'Query execution error'}
    return {'status': 200, 
            'data': menuItems}