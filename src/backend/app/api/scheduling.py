from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.user import User
from app.models.time_slot import TimeSlot
from app.schemas.time_slot import TimeSlotCreate, TimeSlotRead, TimeSlotUpdate
from app.api.auth import get_current_user
from app.services.permission_service import has_permission

router = APIRouter(prefix="/scheduling", tags=["scheduling"])

@router.post("/slots", response_model=TimeSlotRead, status_code=201)
def create_time_slot(
    slot_data: TimeSlotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_scheduling"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les créneaux")

    existing = db.query(TimeSlot).filter(
        TimeSlot.tenant_id == current_user.tenant_id,
        TimeSlot.start_time == slot_data.start_time,
        TimeSlot.end_time == slot_data.end_time
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Un créneau identique existe déjà")

    slot = TimeSlot(
        tenant_id=current_user.tenant_id,
        start_time=slot_data.start_time,
        end_time=slot_data.end_time,
        capacity=slot_data.capacity,
        active=slot_data.active
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot

@router.get("/slots", response_model=List[TimeSlotRead])
def list_time_slots(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(TimeSlot).filter(TimeSlot.tenant_id == current_user.tenant_id)
    if active_only:
        query = query.filter(TimeSlot.active == True)
    if start:
        query = query.filter(TimeSlot.start_time >= start)
    if end:
        query = query.filter(TimeSlot.end_time <= end)
    return query.all()

@router.get("/slots/{slot_id}", response_model=TimeSlotRead)
def get_time_slot(
    slot_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    slot = db.query(TimeSlot).filter(
        TimeSlot.id == slot_id,
        TimeSlot.tenant_id == current_user.tenant_id
    ).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Créneau introuvable")
    return slot

@router.patch("/slots/{slot_id}", response_model=TimeSlotRead)
def update_time_slot(
    slot_id: UUID,
    slot_data: TimeSlotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_scheduling"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les créneaux")
    slot = db.query(TimeSlot).filter(
        TimeSlot.id == slot_id,
        TimeSlot.tenant_id == current_user.tenant_id
    ).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Créneau introuvable")

    for field, value in slot_data.dict(exclude_unset=True).items():
        setattr(slot, field, value)

    db.commit()
    db.refresh(slot)
    return slot

@router.delete("/slots/{slot_id}", status_code=204)
def delete_time_slot(
    slot_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_scheduling"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les créneaux")
    slot = db.query(TimeSlot).filter(
        TimeSlot.id == slot_id,
        TimeSlot.tenant_id == current_user.tenant_id
    ).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Créneau introuvable")
    db.delete(slot)
    db.commit()
    return None

@router.get("/check")
def check_availability(
    date: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start = date
    end = date + timedelta(days=1)
    slots = db.query(TimeSlot).filter(
        TimeSlot.tenant_id == current_user.tenant_id,
        TimeSlot.active == True,
        TimeSlot.start_time >= start,
        TimeSlot.start_time <= end
    ).all()

    result = []
    for slot in slots:
        remaining = slot.capacity - slot.booked_count
        result.append({
            "id": str(slot.id),
            "start_time": slot.start_time.isoformat(),
            "end_time": slot.end_time.isoformat(),
            "capacity": slot.capacity,
            "booked_count": slot.booked_count,
            "remaining": max(remaining, 0),
            "available": remaining > 0
        })
    return result