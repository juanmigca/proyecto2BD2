from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

def default_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Status(str, Enum):
    COMPLETED = "Entregado"
    PENDING = "En Camino"
    CANCELED = "Cancelado"



class Location(BaseModel):
    type: Optional[str] = None
    coordinates: Optional[List[float]] = None
    
    
class Ingredient(BaseModel):
    #id: Optional[int] = None
    name: Optional[str] = None
    amount: Optional[float] = 0.0
    unitMeasure: Optional[str] = None

class Cuisines(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = Field(default_factory=default_datetime)
    
    
class MenuItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    ingredients: Optional[List[Ingredient]] = None
    addedToMenu: Optional[str] = Field(default_factory=default_datetime)
    
class Restaurant(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    cuisines: Optional[List[str]] = None
    location: Optional[Location] = None
    menuItems: Optional[List[MenuItem]] = None
    rating: Optional[float] = 0.0
    numReviews: Optional[int] = 0

class User(BaseModel): 
    id: Optional[int] = None
    username: Optional[str] = None
    numOrders: Optional[int] = 0
    numReviews: Optional[int] = 0
    visitedRestaurants: Optional[List[int]] = []

class Order(BaseModel):
    id: Optional[int] = None
    userId: Optional[int] = None
    orderedAt: Optional[str] = Field(default_factory=default_datetime)
    arrivedAt: Optional[str] = None
    status: Optional[Status] = Status.PENDING
    restaurantId: Optional[int] = None
    items: Optional[List[MenuItem]] = []
    subtotal: Optional[float] = 0.0
    tax: Optional[float] = 0.0
    tip: Optional[float] = 0.0
    total: Optional[float] = 0.0
    
class Review(BaseModel):
    id: Optional[int] = None
    userId: Optional[int] = None
    restaurantId: Optional[int] = None
    orderId: Optional[int] = None
    stars: Optional[int] = Field(default=None, ge=1, le=10)
    comment: Optional[str] = None
    timestamp: Optional[str] = Field(default_factory=default_datetime)
    


    
    
    
    