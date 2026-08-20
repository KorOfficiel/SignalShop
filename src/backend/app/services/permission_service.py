from sqlalchemy.orm import Session
from app.models.user import User
from app.models.configuration import Configuration

def has_permission(db: Session, user: User, permission: str) -> bool:
    """Vérifie si l'utilisateur a une permission donnée."""
    if user.role == "OWNER":
        return True  # OWNER a toujours toutes les permissions

    config = db.query(Configuration).filter(
        Configuration.tenant_id == user.tenant_id,
        Configuration.key == "role_permissions"
    ).first()

    if config:
        permissions = config.value.get(user.role, {})
    else:
        default_permissions = {
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
            },
        }
        permissions = default_permissions.get(user.role, {})

    return permissions.get(permission, False)
