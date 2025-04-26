from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import getMongoClient, getCollection
from contextlib import asynccontextmanager
from restaurant import getRestaurants, updateRestaurant, createRestaurant
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

@app.get("/root")
def read_root():
    return {'Status': 'Activo.'}

### Restaurants

@app.get("/restaurants")
def get_restaurants(id: Union[str, list, None] = None, name: Union[str, list, None] = None, cuisine: Union[str, list, None] = None):
    """
    Returns a list of restaurants.
    """
    restaurant_collection = getCollection(mongo_client, 'proyecto2bd', 'restaurants')
    if restaurant_collection is None:
        return {'status': 502,
                'message': 'Error connecting to collection'}
    
    
    try:
        restaurants = getRestaurants(restaurant_collection, id, name, cuisine)
    except:
        return {'status': 500,
                'message': 'Query execution error'}
    return {'status': 200, 
            'data': list[restaurants]}

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
        updateRestaurant({restaurant_id}, restaurant_collection)
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
    







