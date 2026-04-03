from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
from pydantic import BaseModel
import httpx

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

USER_SERVICE_URL = "http://localhost:8001"
PRODUCT_SERVICE_URL = "http://localhost:8002"


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "order service running"}


@app.post("/orders")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):

    async with httpx.AsyncClient() as client:

        # Validate user
        user_res = await client.get(
            f"{USER_SERVICE_URL}/users/{order.user_id}"
        )
        if user_res.status_code != 200 or user_res.json() is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate product
        product_res = await client.get(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}"
        )
        if product_res.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")

    db_order = models.Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


@app.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()
