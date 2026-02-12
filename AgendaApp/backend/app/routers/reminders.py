from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..auth import get_current_user
from ..database import get_db
from ..models import Reminder, User

router = APIRouter(prefix="/api/reminders", tags=["reminders"])


@router.post("", response_model=schemas.ReminderOut, status_code=201)
def create_reminder(
    payload: schemas.ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reminder = Reminder(owner_id=current_user.id, **payload.model_dump())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


@router.get("", response_model=list[schemas.ReminderOut])
def list_reminders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Reminder).filter(Reminder.owner_id == current_user.id).all()


@router.put("/{reminder_id}", response_model=schemas.ReminderOut)
def update_reminder(
    reminder_id: int,
    payload: schemas.ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.owner_id == current_user.id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(reminder, key, value)
    db.commit()
    db.refresh(reminder)
    return reminder


@router.delete("/{reminder_id}", status_code=204)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.owner_id == current_user.id).first()
    if reminder:
        db.delete(reminder)
        db.commit()
