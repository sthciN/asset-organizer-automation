from app import app
from typing import Union
from pydantic import BaseModel
# from dotenv import load_dotenv
from process import provider
import logging

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Healthcheck": "OK"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/def-endpoint")
def test_endpoint():
    provider()
    return 'ok'

    