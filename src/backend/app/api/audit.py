from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User
from app.models.audit_event import AuditEvent
from app.api.auth import get_current_user
from app.services.permission_service import has_permission

router = APIRouter(prefix="/audit", tags=["audit"])

class AuditEventRead(BaseModel):
    id: UUID
    tenant_id: UUID
    user_id: Optional[UUID]
    action: str
    entity_type: Optional[str]
    entity_id: Optional[str]
    details: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("", response_model=List[AuditEventRead])
def list_audit_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste les 100 derniers événements d'audit du tenant."""
    if not has_permission(db, current_user, "view_audit"):
        raise HTTPException(status_code=403, detail="Permission manquante : consulter l'audit")

    events = db.query(AuditEvent).filter(
        AuditEvent.tenant_id == current_user.tenant_id
    ).order_by(AuditEvent.created_at.desc()).limit(100).all()
    return events