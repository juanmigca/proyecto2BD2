from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import string
import random
import json
import os
import pickle

app = FastAPI()

