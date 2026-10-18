import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Plain settings come from a ConfigMap, the secret from Key Vault (both arrive as env vars)
APP_ENV = os.getenv("APP_ENV", "local")
WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Hello from my API!")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI(title="My Python Web API App")

# In-memory store (resets when the app restarts)
items: dict[int, dict] = {}
next_id = 1


class ItemIn(BaseModel):
    name: str
    price: float


@app.get("/")
def home():
    return {"message": WELCOME_MESSAGE}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config")
def config():
    # Never return the secret itself, only whether it was loaded
    return {
        "app_env": APP_ENV,
        "welcome_message": WELCOME_MESSAGE,
        "db_password_loaded": DB_PASSWORD is not None,
        "db_password_length": len(DB_PASSWORD) if DB_PASSWORD else 0,
    }


@app.get("/items")
def list_items():
    return list(items.values())


@app.post("/items", status_code=201)
def create_item(item: ItemIn):
    global next_id
    new_item = {"id": next_id, **item.model_dump()}
    items[next_id] = new_item
    next_id += 1
    return new_item


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
