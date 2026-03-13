from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

products = []

class Product(BaseModel):
    name: str
    price: float

@app.get("/health")
def health():
    return {"status": "product service running"}

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return {"message": "product added"}

@app.get("/products")
def list_products():
    return products
