from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_tables
from app.scheduler import start_scheduler, stop_scheduler
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()


app = FastAPI(
    title="Reminder API",
    description="A full-featured reminder system with email notifications. Create reminders and get notified at the scheduled time.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Reminder API is running!",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}