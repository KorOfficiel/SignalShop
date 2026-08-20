from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.models.notification import Notification
from app.api.auth import get_current_user
from app.services.permission_service import has_permission
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/notifications", tags=["notifications"])

class NotificationRead(BaseModel):
    id: UUID
    type: str
    message: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("", response_model=List[NotificationRead])
def list_notifications(
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_notifications"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les notifications")
    query = db.query(Notification).filter(Notification.tenant_id == current_user.tenant_id)
    if unread_only:
        query = query.filter(Notification.read == False)
    return query.order_by(Notification.created_at.desc()).all()

@router.patch("/{notification_id}/read", response_model=NotificationRead)
def mark_as_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_notifications"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les notifications")
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.tenant_id == current_user.tenant_id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification introuvable")
    notification.read = True
    db.commit()
    db.refresh(notification)
    return notification

@router.patch("/read-all", response_model=dict)
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_notifications"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les notifications")
    db.query(Notification).filter(
        Notification.tenant_id == current_user.tenant_id,
        Notification.read == False
    ).update({"read": True})
    db.commit()
    return {"status": "all read"}

@router.delete("/{notification_id}", status_code=204)
def delete_notification(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime une notification spécifique."""
    if not has_permission(db, current_user, "manage_notifications"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les notifications")
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.tenant_id == current_user.tenant_id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification introuvable")
    db.delete(notification)
    db.commit()
    return None

@router.delete("", status_code=204)
def delete_all_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime toutes les notifications du tenant."""
    if not has_permission(db, current_user, "manage_notifications"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les notifications")
    db.query(Notification).filter(
        Notification.tenant_id == current_user.tenant_id
    ).delete()
    db.commit()
    return None