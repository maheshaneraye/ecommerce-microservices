from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
from pydantic import BaseModel

app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json"
        )  # ✅ no root_path


models.Base.metadata.create_all(bind=database.engine)


class ProductCreate(BaseModel):
    name: str
    price: float


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "product service running"}


@app.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(name=product.name, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@app.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
