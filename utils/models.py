from pydantic import BaseModel, Field
from typing import List, Optional
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
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    
    
class MenuItem(BaseModel):
    id: int
    name: str
    price: float
    ingredients: List[Ingredient] 
    addedToMenu: Optional[str] = None
    
class Restaurant(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    cuisines: Optional[List[str]] = None
    location: Optional[Location] = None
    menuItems: Optional[List[MenuItem]] = None
    rating: Optional[float] = 0
    numReviews: Optional[int] = 0

class User(BaseModel): 
    id: int
    username: str
    numOrders: int = 0
    numReviews: int = 0
    visitedRestaurants: Optional[List[str]] = None

class Order(BaseModel):
    id: int
    userId: str
    orderedAt: str
    arrivedAt: str
    status: Status 
    restaurantId: str
    items: List[MenuItem]
    subtotal: float
    tax: float
    tip: float
    total: float
    
class Review(BaseModel):
    id: int
    userId: str
    restaurantId: Optional[str] = None
    orderId: Optional[str] = None
    stars: int = Field(..., ge=1, le=10)
    comment: str
    timestamp: str
    
def encoder(obj):
    if isinstance(obj, str):
        return obj.isoformat()
    elif isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Type {type(obj)} not serializable")

    
    
    
    