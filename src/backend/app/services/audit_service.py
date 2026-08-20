from sqlalchemy.orm import Session
from app.models.audit_event import AuditEvent
from app.models.user import User

def log_audit(db: Session, user: User, action: str, entity_type: str = None, entity_id: str = None, details: dict = None):
    event = AuditEvent(
        tenant_id=user.tenant_id,
        user_id=user.id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )
    db.add(event)