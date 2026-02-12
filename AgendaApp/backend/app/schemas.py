from datetime import date, time

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str


class EventBase(BaseModel):
    title: str
    date: date
    start_time: time
    end_time: time
    location: str | None = None
    category: str
    notes: str | None = None
    recurrence: str | None = None
    recurrence_rule: str | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = None
    date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    location: str | None = None
    category: str | None = None
    notes: str | None = None
    recurrence: str | None = None
    recurrence_rule: str | None = None


class EventOut(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    color: str


class TaskBase(BaseModel):
    title: str
    due_date: date | None = None
    priority: str = "medium"
    notes: str | None = None
    event_id: int | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    due_date: date | None = None
    priority: str | None = None
    notes: str | None = None
    is_done: bool | None = None
    event_id: int | None = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    is_done: bool


class ReminderBase(BaseModel):
    event_id: int | None = None
    task_id: int | None = None
    minutes_before: int = Field(ge=0)
    custom_message: str | None = None
    daily_summary: bool = False


class ReminderCreate(ReminderBase):
    pass


class ReminderUpdate(BaseModel):
    minutes_before: int | None = Field(default=None, ge=0)
    custom_message: str | None = None
    daily_summary: bool | None = None


class ReminderOut(ReminderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
