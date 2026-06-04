from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class ReminderCreate(BaseModel):
    title: str
    message: str
    email: EmailStr
    remind_at: datetime

    @field_validator("remind_at")
    @classmethod
    def remind_at_must_be_future(cls, v):
        if v <= datetime.now():
            raise ValueError("remind_at must be a future datetime")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Doctor Appointment",
                "message": "Don't forget your 3pm appointment!",
                "email": "user@example.com",
                "remind_at": "2025-12-31T15:00:00"
            }
        }
    }


class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    email: Optional[EmailStr] = None
    remind_at: Optional[datetime] = None

    @field_validator("remind_at")
    @classmethod
    def remind_at_must_be_future(cls, v):
        if v and v <= datetime.now():
            raise ValueError("remind_at must be a future datetime")
        return v


class ReminderResponse(BaseModel):
    id: int
    title: str
    message: str
    email: str
    remind_at: datetime
    is_sent: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}