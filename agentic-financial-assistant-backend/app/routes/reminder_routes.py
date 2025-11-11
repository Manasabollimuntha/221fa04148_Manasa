from fastapi import APIRouter, HTTPException
from app.db import reminders_collection
from datetime import datetime

router = APIRouter(prefix="/reminder", tags=["Reminders"])

@router.post("/add")
def add_reminder(reminder: dict):
    title = reminder.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="Reminder title is required")

    reminder_doc = {
        "title": title,
        "send_at": datetime.utcnow().isoformat()
    }
    reminders_collection.insert_one(reminder_doc)
    return reminder_doc

@router.get("/list")
def get_reminders():
    reminders = list(reminders_collection.find({}, {"_id": 0}))
    return reminders
