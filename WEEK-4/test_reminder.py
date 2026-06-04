"""
tests/test_reminders.py
Run with: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from app.main import app
from app.database import Base, get_db

# ── Use an in-memory SQLite DB for tests ──────────────────────
TEST_DATABASE_URL = "sqlite:///./test_reminders.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

FUTURE_TIME = (datetime.now() + timedelta(hours=2)).isoformat()


def make_reminder(title="Test Reminder"):
    return {
        "title": title,
        "message": "Test message body",
        "email": "test@example.com",
        "remind_at": FUTURE_TIME,
    }


# ── Tests ──────────────────────────────────────────────────────

def test_health_check():
    r = client.get("/")
    assert r.status_code == 200
    assert "running" in r.json()["message"]


def test_create_reminder():
    r = client.post("/reminders/", json=make_reminder())
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test Reminder"
    assert data["is_sent"] is False
    assert "id" in data


def test_list_reminders():
    client.post("/reminders/", json=make_reminder("Reminder A"))
    client.post("/reminders/", json=make_reminder("Reminder B"))
    r = client.get("/reminders/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 2


def test_get_single_reminder():
    created = client.post("/reminders/", json=make_reminder()).json()
    r = client.get(f"/reminders/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_get_nonexistent_reminder():
    r = client.get("/reminders/999999")
    assert r.status_code == 404


def test_update_reminder():
    created = client.post("/reminders/", json=make_reminder()).json()
    r = client.put(f"/reminders/{created['id']}", json={"title": "Updated Title"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated Title"


def test_delete_reminder():
    created = client.post("/reminders/", json=make_reminder()).json()
    r = client.delete(f"/reminders/{created['id']}")
    assert r.status_code == 204
    # Confirm it's gone
    r2 = client.get(f"/reminders/{created['id']}")
    assert r2.status_code == 404


def test_past_remind_at_rejected():
    past_time = (datetime.now() - timedelta(hours=1)).isoformat()
    payload = {**make_reminder(), "remind_at": past_time}
    r = client.post("/reminders/", json=payload)
    assert r.status_code == 422  # Validation error


def test_invalid_email_rejected():
    payload = {**make_reminder(), "email": "not-an-email"}
    r = client.post("/reminders/", json=payload)
    assert r.status_code == 422