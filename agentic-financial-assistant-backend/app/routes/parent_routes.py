# app/routes/parent_routes.py
from fastapi import APIRouter, Depends
from app.auth import get_current_parent
from app.schemas import TokenOut

router = APIRouter(prefix="/parent", tags=["parent"])

@router.get("/me")
async def me(current_parent: dict = Depends(get_current_parent)):
    # convert ObjectId to str for _id
    current_parent["_id"] = str(current_parent["_id"])
    # don't return hashed password
    current_parent.pop("hashed_password", None)
    return current_parent
