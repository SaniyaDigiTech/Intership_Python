from sqlalchemy.orm import Session
from datetime import datetime
from app.database import Reminder
from app.schemas import ReminderCreate, ReminderUpdate

def create_reminder(db: Session, data: ReminderCreate):
    reminder = Reminder(**data.model_dump())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def get_reminder(db: Session, reminder_id: int):
    return db.query(Reminder).filter(Reminder.id == reminder_id).first()

def get_all_reminders(db: Session, skip=0, limit=20, active_only=False):
    query = db.query(Reminder)
    if active_only:
        query = query.filter(Reminder.is_active == True)
    total = query.count()
    return total, query.order_by(Reminder.remind_at).offset(skip).limit(limit).all()

def update_reminder(db: Session, reminder_id: int, data: ReminderUpdate):
    reminder = get_reminder(db, reminder_id)
    if not reminder:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(reminder, field, value)
    if "remind_at" in data.model_dump(exclude_unset=True):
        reminder.is_sent = False
    reminder.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(reminder)
    return reminder

def delete_reminder(db: Session, reminder_id: int):
    reminder = get_reminder(db, reminder_id)
    if not reminder:
        return False
    db.delete(reminder)
    db.commit()
    return True