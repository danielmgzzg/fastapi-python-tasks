from typing import Optional

from fastapi import FastAPI
from .connection import db

app = FastAPI()


# Our root endpoint
@app.get("/")
def index():
    return {"message": "Hello World"}

# Signup endpoint with the POST method
