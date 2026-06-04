"""
scheduler.py
Runs in a background thread. Every 60 seconds it checks for reminders
that are due (remind_at <= now and is_sent == False) and sends them.
"""

import threading
import time
from datetime import datetime

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Reminder
from app.email_service import send_reminder_email


def process_due_reminders():
    """Query and send all due, unsent reminders."""
    db: Session = SessionLocal()
    try:
        due = (
            db.query(Reminder)
            .filter(Reminder.remind_at <= datetime.now(), Reminder.is_sent == False)
            .all()
        )
        for reminder in due:
            success = send_reminder_email(
                to_email=reminder.email,
                title=reminder.title,
                message=reminder.message,
                remind_at=reminder.remind_at,
            )
            if success:
                reminder.is_sent = True
                db.commit()
                print(f"[SCHEDULER] Reminder #{reminder.id} marked as sent.")
            else:
                print(f"[SCHEDULER] Failed to send reminder #{reminder.id}.")
    finally:
        db.close()


def start_scheduler(interval_seconds: int = 60):
    """Start the background scheduler thread."""

    def run():
        print(f"[SCHEDULER] Started — checking every {interval_seconds}s")
        while True:
            try:
                process_due_reminders()
            except Exception as e:
                print(f"[SCHEDULER] Error: {e}")
            time.sleep(interval_seconds)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()