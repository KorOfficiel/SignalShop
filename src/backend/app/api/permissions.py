from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.configuration import Configuration
from app.api.auth import get_current_user

router = APIRouter(prefix="/permissions", tags=["permissions"])

DEFAULT_PERMISSIONS = {
    "OWNER": {
        "manage_products": True,
        "manage_categories": True,
        "manage_orders": True,
        "manage_users": True,
        "manage_settings": True,
        "view_conversations": True,
        "take_handoff": True,
        "manage_customers": True,
        "manage_scheduling": True,
        "manage_delivery": True,
        "manage_ratings": True,
        "manage_notifications": True,
        "export_orders": True,
        "view_statistics": True,
        "view_audit": True,
    },
    "ADMIN": {
        "manage_products": True,
        "manage_categories": True,
        "manage_orders": True,
        "manage_users": True,
        "manage_settings": True,
        "view_conversations": True,
        "take_handoff": True,
        "manage_customers": True,
        "manage_scheduling": True,
        "manage_delivery": True,
        "manage_ratings": True,
        "manage_notifications": True,
        "export_orders": True,
        "view_statistics": True,
        "view_audit": True,
    },
    "MANAGER": {
        "manage_products": True,
        "manage_categories": True,
        "manage_orders": True,
        "manage_users": False,
        "manage_settings": False,
        "view_conversations": True,
        "take_handoff": True,
        "manage_customers": True,
        "manage_scheduling": True,
        "manage_delivery": True,
        "manage_ratings": True,
        "manage_notifications": True,
        "export_orders": True,
        "view_statistics": True,
        "view_audit": False,
    },
    "STAFF": {
        "manage_products": False,
        "manage_categories": False,
        "manage_orders": False,
        "manage_users": False,
        "manage_settings": False,
        "view_conversations": True,
        "take_handoff": True,
        "manage_customers": False,
        "manage_scheduling": False,
        "manage_delivery": False,
        "manage_ratings": False,
        "manage_notifications": False,
        "export_orders": False,
        "view_statistics": False,
        "view_audit": False,
    },
}

@router.get("")
def get_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    config = db.query(Configuration).filter(
        Configuration.tenant_id == current_user.tenant_id,
        Configuration.key == "role_permissions"
    ).first()
    if config:
        return config.value
    return DEFAULT_PERMISSIONS

@router.put("")
def update_permissions(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "OWNER":
        raise HTTPException(status_code=403, detail="Seul le propriétaire peut modifier les permissions")

    config = db.query(Configuration).filter(
        Configuration.tenant_id == current_user.tenant_id,
        Configuration.key == "role_permissions"
    ).first()
    if config:
        config.value = payload
    else:
        config = Configuration(
            tenant_id=current_user.tenant_id,
            key="role_permissions",
            value=payload
        )
        db.add(config)
    db.commit()
    return payload