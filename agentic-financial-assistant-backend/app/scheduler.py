# app/scheduler.py
import asyncio
import logging
from datetime import datetime
from app.db import get_reminders_collection, get_parents_collection
from app.email_utils import send_email

log = logging.getLogger(__name__)

async def check_and_send_due_reminders_once():
    reminders = get_reminders_collection()
    parents = get_parents_collection()
    now = datetime.utcnow()
    cursor = reminders.find({"sent": False, "send_at": {"$lte": now}})
    async for rem in cursor:
        try:
            parent = await parents.find_one({"_id": rem["parent_id"]}) if rem.get("parent_id") else None
            # If parent is stored as ObjectId, you may need to query by ObjectId
            # parent = await parents.find_one({"_id": rem["parent_id"]})
            email = parent.get("email") if parent else None
            if email:
                sent = send_email(email, rem.get("title", "Reminder"), rem.get("message", ""))
                if sent:
                    await reminders.update_one({"_id": rem["_id"]}, {"$set": {"sent": True}})
                    log.info("Reminder sent: %s -> %s", rem["_id"], email)
                else:
                    log.info("Email not sent for reminder %s (email send returned False)", rem["_id"])
            else:
                log.info("No email for reminder %s; skipping", rem["_id"])
        except Exception as e:
            log.exception("Error processing reminder %s: %s", rem.get("_id"), e)

async def reminder_worker(stop_event: asyncio.Event):
    log.info("Reminder worker started")
    while not stop_event.is_set():
        try:
            await check_and_send_due_reminders_once()
        except Exception as e:
            log.exception("Reminder worker error: %s", e)
        # wait 60 seconds or until stop_event is set
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=60.0)
        except asyncio.TimeoutError:
            continue
    log.info("Reminder worker stopped")
