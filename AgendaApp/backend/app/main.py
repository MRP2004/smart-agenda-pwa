from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, events, reminders, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Agenda API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(tasks.router)
app.include_router(reminders.router)


@app.get("/api/health")
def healthcheck():
    return {"status": "ok"}
