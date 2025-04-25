from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import string
import random
import json
import os
import pickle

app = FastAPI()

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


@app.get("/resturants/get_one")
def get_one_resturant(id: int, name: int, address: str, phone: str, email: str):
    return {'Status': 'Activo.'}

@app.get("/resturants/get_many")
def get_all_resturants(id: int):
    return {'Status': 'Activo.'}




