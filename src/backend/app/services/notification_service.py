from sqlalchemy.orm import Session
from app.models.notification import Notification

def create_notification(db: Session, tenant_id, type: str, message: str):
    """Crée une notification pour le tenant."""
    notification = Notification(
        tenant_id=tenant_id,
        type=type,
        message=message,
        read=False
    )
    db.add(notification)