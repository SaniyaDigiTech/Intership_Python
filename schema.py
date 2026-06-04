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
    def must_be_future(cls, v):
        if v <= datetime.utcnow():
            raise ValueError("remind_at must be a future datetime")
        return v

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    email: Optional[EmailStr] = None
    remind_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class ReminderResponse(BaseModel):
    id: int
    title: str
    message: str
    email: str
    remind_at: datetime
    is_sent: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class ReminderListResponse(BaseModel):
    total: int
    reminders: list[ReminderResponse]

class MessageResponse(BaseModel):
    message: str