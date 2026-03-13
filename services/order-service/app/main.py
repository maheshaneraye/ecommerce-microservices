from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

orders = []

class Order(BaseModel):
    user_id: int
    product_id: int
    quantity: int

@app.get("/health")
def health():
    return {"status": "order service running"}

@app.post("/orders")
def create_order(order: Order):
    orders.append(order)
    return {"message": "order created"}

@app.get("/orders")
def list_orders():
    return orders
