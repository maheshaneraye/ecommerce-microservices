from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import database
from pydantic import BaseModel

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


class UserCreate(BaseModel):
    email: str
    password: str


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "user service running"}


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()
