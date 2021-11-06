from typing import Optional

from fastapi import FastAPI
from .connection import collection

app = FastAPI()


# Our root endpoint
@app.get("/")
def index():
    return {"message": "Hello Worlds"}

# Signup endpoint with the POST method
