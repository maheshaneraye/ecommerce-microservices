from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    email: str
    password: str

@app.get("/health")
def health():
    return {"status": "user service running"}

@app.post("/register")
def register(user: User):
    users.append(user)
    return {"message": "user registered"}

@app.get("/users")
def get_users():
    return users
