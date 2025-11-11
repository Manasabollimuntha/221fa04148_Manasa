from fastapi import APIRouter, HTTPException
from app.auth import hash_password, verify_password, create_access_token
from app.db import parents_collection

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register_user(data: dict):
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")

    if not all([email, name, password]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    if parents_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(password)
    parents_collection.insert_one({"name": name, "email": email, "password": hashed})
    return {"message": "Registration successful"}

@router.post("/login")
def login_user(data: dict):
    email = data.get("email")
    password = data.get("password")

    user = parents_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": email})
    return {"access_token": token, "token_type": "bearer"}
