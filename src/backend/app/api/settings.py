from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.configuration import Configuration
from app.api.auth import get_current_user
from app.services.permission_service import has_permission

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("")
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    configs = db.query(Configuration).filter(Configuration.tenant_id == current_user.tenant_id).all()
    result = {
        "app_name": "SignalShop",
        "sound_enabled": True,
        "welcome_message": "Bonjour ! Bienvenue chez SignalShop. Comment puis-je vous aider ?",
        "tone": "vous",
        "signal_service_phone": "",
    }
    for config in configs:
        result[config.key] = config.value
    return result

@router.put("")
def update_settings(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_settings"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les paramètres")

    for key, value in payload.items():
        config = db.query(Configuration).filter(
            Configuration.tenant_id == current_user.tenant_id,
            Configuration.key == key
        ).first()
        if config:
            config.value = value
        else:
            config = Configuration(
                tenant_id=current_user.tenant_id,
                key=key,
                value=value
            )
            db.add(config)
    db.commit()
    return payload