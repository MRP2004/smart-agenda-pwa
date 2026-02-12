from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    events = relationship("Event", back_populates="owner", cascade="all,delete")
    tasks = relationship("Task", back_populates="owner", cascade="all,delete")
    reminders = relationship("Reminder", back_populates="owner", cascade="all,delete")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)
    location: Mapped[str | None] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    recurrence: Mapped[str | None] = mapped_column(String(50))
    recurrence_rule: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="events")
    tasks = relationship("Task", back_populates="event")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    event_id: Mapped[int | None] = mapped_column(ForeignKey("events.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    due_date: Mapped[Date | None] = mapped_column(Date)
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    notes: Mapped[str | None] = mapped_column(Text)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)

    owner = relationship("User", back_populates="tasks")
    event = relationship("Event", back_populates="tasks")


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    event_id: Mapped[int | None] = mapped_column(ForeignKey("events.id"), nullable=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"), nullable=True)
    minutes_before: Mapped[int] = mapped_column(Integer, nullable=False)
    custom_message: Mapped[str | None] = mapped_column(String(255))
    daily_summary: Mapped[bool] = mapped_column(Boolean, default=False)

    owner = relationship("User", back_populates="reminders")
