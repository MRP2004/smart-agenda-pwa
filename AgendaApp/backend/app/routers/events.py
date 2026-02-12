from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..auth import get_current_user
from ..database import get_db
from ..models import Event, User

router = APIRouter(prefix="/api/events", tags=["events"])

CATEGORY_COLORS = {
    "subject": "#2563eb",
    "practice": "#16a34a",
    "exam": "#dc2626",
    "personal": "#9333ea",
}


@router.post("", response_model=schemas.EventOut, status_code=201)
def create_event(
    payload: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = Event(
        owner_id=current_user.id,
        color=CATEGORY_COLORS.get(payload.category.lower(), "#0f766e"),
        **payload.model_dump(),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("", response_model=list[schemas.EventOut])
def list_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    q: str | None = None,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    upcoming_days: int | None = None,
):
    query = db.query(Event).filter(Event.owner_id == current_user.id)
    if q:
        like = f"%{q}%"
        query = query.filter((Event.title.ilike(like)) | (Event.notes.ilike(like)) | (Event.location.ilike(like)))
    if category:
        query = query.filter(Event.category == category)
    if start_date:
        query = query.filter(Event.date >= start_date)
    if end_date:
        query = query.filter(Event.date <= end_date)
    if upcoming_days:
        today = date.today()
        query = query.filter(Event.date.between(today, today + timedelta(days=upcoming_days)))
    return query.order_by(Event.date, Event.start_time).all()


@router.put("/{event_id}", response_model=schemas.EventOut)
def update_event(
    event_id: int,
    payload: schemas.EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(event, key, value)

    if "category" in updates:
        event.color = CATEGORY_COLORS.get(event.category.lower(), "#0f766e")

    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if event:
        db.delete(event)
        db.commit()
