from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    message = Column(String(1000), nullable=False)
    email = Column(String(255), nullable=False)
    remind_at = Column(DateTime, nullable=False)        # When to send the reminder
    is_sent = Column(Boolean, default=False)            # Has the email been sent?
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())