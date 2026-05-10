import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from jose import jwt, JWTError
import httpx

# CONFIG 

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@postgres:5432/ecommerce"
)

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://product-service:8000"
)

# DB SETUP 

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# MODEL (DB) 

class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)


Base.metadata.create_all(bind=engine)

# SCHEMA 

class Order(BaseModel):
    user_id: int
    product_id: int
    quantity: int

# APP 

app = FastAPI(
        root_path="/orders"
        )

#  DB DEPENDENCY 

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# SECURITY 

security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload["sub"]

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

# PRODUCT VALIDATION 

async def validate_product(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PRODUCT_SERVICE_URL}/{product_id}"
        )

        return response.status_code == 200

# ROUTES 

@app.get("/health")
def health():
    return {
        "status": "order service running"
    }


@app.post("/")
async def create_order(
    order: Order,
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    valid = await validate_product(order.product_id)

    if not valid:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    new_order = OrderDB(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "message": "order created",
        "order_id": new_order.id
    }


@app.get("/")
def list_orders(
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    orders = db.query(OrderDB).all()

    return [
        {
            "id": o.id,
            "user_id": o.user_id,
            "product_id": o.product_id,
            "quantity": o.quantity
        }
        for o in orders
    ]


@app.get("/{order_id}")
def get_order(
    order_id: int,
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    order = db.query(OrderDB).filter(
        OrderDB.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "id": order.id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity
    }
