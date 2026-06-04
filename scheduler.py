from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Reminder
from app.email_service import send_reminder_email

scheduler = BackgroundScheduler()


def check_and_send_reminders():
    """Check for due reminders and send email notifications."""
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        due_reminders = (
            db.query(Reminder)
            .filter(
                Reminder.remind_at <= now,
                Reminder.is_sent == False,
                Reminder.is_active == True,
            )
            .all()
        )

        for reminder in due_reminders:
            print(f"[SCHEDULER] Processing reminder ID={reminder.id}: '{reminder.title}'")
            success = send_reminder_email(
                to_email=reminder.email,
                title=reminder.title,
                message=reminder.message,
                remind_at=reminder.remind_at,
            )
            if success:
                reminder.is_sent = True
                reminder.updated_at = datetime.utcnow()
                db.commit()
                print(f"[SCHEDULER] Reminder ID={reminder.id} marked as sent.")
            else:
                print(f"[SCHEDULER] Failed to send reminder ID={reminder.id}. Will retry.")

    except Exception as e:
        print(f"[SCHEDULER ERROR] {e}")
        db.rollback()
    finally:
        db.close()


def start_scheduler():
    """Start the background scheduler (checks every 60 seconds)."""
    scheduler.add_job(
        check_and_send_reminders,
        trigger=IntervalTrigger(seconds=60),
        id="reminder_check",
        name="Check and send due reminders",
        replace_existing=True,
    )
    scheduler.start()
    print("[SCHEDULER] Started — checking reminders every 60 seconds.")


def stop_scheduler():
    """Gracefully stop the scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        print("[SCHEDULER] Stopped.")