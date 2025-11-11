# app/email_utils.py
import smtplib
from email.message import EmailMessage
from app.config import settings
import logging

log = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, body: str) -> bool:
    # If SMTP not configured, skip sending (helpful for dev)
    if not (settings.email_user and settings.email_pass and settings.smtp_server and settings.smtp_port):
        log.info("Email config missing: skipping send")
        return False

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.email_user
        msg["To"] = to_email
        msg.set_content(body)

        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.email_user, settings.email_pass)
            server.send_message(msg)
        return True
    except Exception as e:
        log.exception("Failed to send email: %s", e)
        return False
