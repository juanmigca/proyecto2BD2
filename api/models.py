from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    COMPLETED = "Entregado"
    PENDING = "En Camino"
    CANCELED = "Cancelado"

class Location(BaseModel):
    type: str 
    coordinates: List[float] 
    
    
class Ingredient(BaseModel):
    name: str
    amount: float
    unitMeasure: str

class Cuisines(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    
class MenuItem(BaseModel):
    id: str
    name: str
    price: float
    ingredients: List[Ingredient] 
    addedToMenu: datetime = Field(default_factory=datetime.now)
    
class Restaurant(BaseModel):
    id: str
    name: str
    address: Optional[str] = None
    cuisines: Optional[List[str]] = None
    location: Optional[Location] = None
    menuItems: Optional[MenuItem] = None
    rating: Optional[float] = None

class User(BaseModel): 
    id: str
    username: str
    numOrders: int = 0
    numReviews: int = 0
    visitedRestaurants: Optional[List[str]] = None

class Order(BaseModel):
    id: str
    userId: str
    orderedAt: datetime
    arrivedAt: datetime
    status: Status 
    resraurantId: str
    items: List[MenuItem]
    subtotal: float
    tax: float
    tip: float
    total: float
    
class Review(BaseModel):
    id: str
    userId: str
    restaurantId: Optional[str] = None
    orederId: Optional[str] = None
    stars: int = Field(..., ge=1, le=10)
    comment: str
    timestamp: datetime
    

    
    
    
    