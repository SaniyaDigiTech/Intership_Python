from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    ReminderCreate,
    ReminderUpdate,
    ReminderResponse,
    ReminderListResponse,
    MessageResponse,
)
from app import crud

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("/", response_model=ReminderResponse, status_code=201)
def create_reminder(data: ReminderCreate, db: Session = Depends(get_db)):
    """Create a new reminder. Email will be sent at the scheduled time."""
    return crud.create_reminder(db, data)


@router.get("/", response_model=ReminderListResponse)
def list_reminders(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    active_only: bool = Query(False, description="Filter to active reminders only"),
    db: Session = Depends(get_db),
):
    """List all reminders with pagination."""
    total, reminders = crud.get_all_reminders(db, skip=skip, limit=limit, active_only=active_only)
    return ReminderListResponse(total=total, reminders=reminders)


@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """Get a single reminder by ID."""
    reminder = crud.get_reminder(db, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail=f"Reminder {reminder_id} not found")
    return reminder


@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(reminder_id: int, data: ReminderUpdate, db: Session = Depends(get_db)):
    """Update an existing reminder. Updating remind_at resets the sent status."""
    reminder = crud.update_reminder(db, reminder_id, data)
    if not reminder:
        raise HTTPException(status_code=404, detail=f"Reminder {reminder_id} not found")
    return reminder


@router.delete("/{reminder_id}", response_model=MessageResponse)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """Permanently delete a reminder."""
    deleted = crud.delete_reminder(db, reminder_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Reminder {reminder_id} not found")
    return MessageResponse(message=f"Reminder {reminder_id} deleted successfully")