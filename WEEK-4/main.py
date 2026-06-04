from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import engine, Base
from app.routers import reminders
from app.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    start_scheduler(interval_seconds=60)
    yield


app = FastAPI(
    title="Reminder API",
    description="A REST API to create and manage reminders with email notifications.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])


@app.get("/", tags=["Health"])
def root():
    return {"message": "Reminder API is running!", "docs": "/docs"}