from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Reminder
from app.schemas import ReminderCreate, ReminderUpdate, ReminderResponse
from app.email_service import send_reminder_email

router = APIRouter()


# ─────────────────────────────────────────────
# POST /reminders   — Create a new reminder
# ─────────────────────────────────────────────
@router.post("/", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    payload: ReminderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Create a new reminder. An email confirmation is sent immediately,
    and the scheduler will send the actual reminder when remind_at is due.
    """
    reminder = Reminder(**payload.model_dump())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    # Send a confirmation email in the background (non-blocking)
    background_tasks.add_task(
        send_reminder_email,
        to_email=reminder.email,
        title=f"✅ Reminder Set: {reminder.title}",
        message=(
            f"Your reminder has been created!\n\n"
            f"Message: {reminder.message}\n"
            f"It will be sent at: {reminder.remind_at}"
        ),
        remind_at=reminder.remind_at,
    )

    return reminder


# ─────────────────────────────────────────────
# GET /reminders   — List all reminders
# ─────────────────────────────────────────────
@router.get("/", response_model=List[ReminderResponse])
def list_reminders(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """Return a paginated list of all reminders."""
    return db.query(Reminder).offset(skip).limit(limit).all()


# ─────────────────────────────────────────────
# GET /reminders/{id}   — Get one reminder
# ─────────────────────────────────────────────
@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """Fetch a single reminder by ID."""
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder


# ─────────────────────────────────────────────
# PUT /reminders/{id}   — Update a reminder
# ─────────────────────────────────────────────
@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    payload: ReminderUpdate,
    db: Session = Depends(get_db),
):
    """Update one or more fields of an existing reminder."""
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    # Only update provided fields (partial update)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(reminder, field, value)

    db.commit()
    db.refresh(reminder)
    return reminder


# ─────────────────────────────────────────────
# DELETE /reminders/{id}   — Delete a reminder
# ─────────────────────────────────────────────
@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """Delete a reminder by ID."""
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    db.delete(reminder)
    db.commit()
    return None


# ─────────────────────────────────────────────
# POST /reminders/{id}/send   — Manually trigger email
# ─────────────────────────────────────────────
@router.post("/{reminder_id}/send", response_model=ReminderResponse)
def send_reminder_now(
    reminder_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Manually trigger sending the email for a reminder (useful for testing)."""
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    background_tasks.add_task(
        send_reminder_email,
        to_email=reminder.email,
        title=reminder.title,
        message=reminder.message,
        remind_at=reminder.remind_at,
    )

    reminder.is_sent = True
    db.commit()
    db.refresh(reminder)
    return reminder