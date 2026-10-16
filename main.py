from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="My Python Web API App")

# In-memory store (resets when the app restarts)
items: dict[int, dict] = {}
next_id = 1


class ItemIn(BaseModel):
    name: str
    price: float


@app.get("/")
def home():
    return {"message": "Hello from my API!"}


@app.get("/health")
def health():
    return {"status": "ok"}


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
