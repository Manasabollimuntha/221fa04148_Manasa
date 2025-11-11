from fastapi import APIRouter, Depends, Request, Header
from app.auth import get_current_parent
from app.schemas import PaymentCreate
from app.payments import create_stripe_payment_intent, verify_stripe_event
from app.db import payments_collection
from datetime import datetime

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create")
async def create_payment(payload: PaymentCreate, parent=Depends(get_current_parent)):
    metadata = {"parent_id": str(parent["_id"]), "student_roll": payload.student_roll}
    intent = await create_stripe_payment_intent(payload.amount, payload.currency, metadata)
    # save minimal payment record
    record = {
        "parent_id": str(parent["_id"]),
        "student_roll": payload.student_roll,
        "amount": payload.amount,
        "currency": payload.currency,
        "stripe_payment_intent": intent["id"],
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    res = await payments_collection.insert_one(record)
    return {"client_secret": intent["client_secret"], "payment_id": str(res.inserted_id)}

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    event = verify_stripe_event(payload, stripe_signature)
    # Handle payment_intent.succeeded etc
    if event and event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        pid = intent["id"]
        await payments_collection.update_one({"stripe_payment_intent": pid}, {"$set": {"status": "succeeded", "updated_at": datetime.utcnow()}})
    return {"status": "ok"}
