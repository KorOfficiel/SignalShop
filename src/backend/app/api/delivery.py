from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.models.delivery_zone import DeliveryZone
from app.schemas.delivery_zone import DeliveryZoneCreate, DeliveryZoneRead, DeliveryZoneUpdate
from app.api.auth import get_current_user
from app.services.permission_service import has_permission

router = APIRouter(prefix="/delivery", tags=["delivery"])

@router.post("/zones", response_model=DeliveryZoneRead, status_code=201)
def create_delivery_zone(
    zone_data: DeliveryZoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_delivery"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer la livraison")
    zone = DeliveryZone(
        tenant_id=current_user.tenant_id,
        name=zone_data.name,
        fee=zone_data.fee,
        min_order=zone_data.min_order,
        active=zone_data.active
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone

@router.get("/zones", response_model=List[DeliveryZoneRead])
def list_delivery_zones(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    zones = db.query(DeliveryZone).filter(DeliveryZone.tenant_id == current_user.tenant_id).all()
    return zones

@router.patch("/zones/{zone_id}", response_model=DeliveryZoneRead)
def update_delivery_zone(
    zone_id: UUID,
    zone_data: DeliveryZoneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_delivery"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer la livraison")
    zone = db.query(DeliveryZone).filter(
        DeliveryZone.id == zone_id,
        DeliveryZone.tenant_id == current_user.tenant_id
    ).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone introuvable")
    for field, value in zone_data.dict(exclude_unset=True).items():
        setattr(zone, field, value)
    db.commit()
    db.refresh(zone)
    return zone

@router.delete("/zones/{zone_id}", status_code=204)
def delete_delivery_zone(
    zone_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_delivery"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer la livraison")
    zone = db.query(DeliveryZone).filter(
        DeliveryZone.id == zone_id,
        DeliveryZone.tenant_id == current_user.tenant_id
    ).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone introuvable")
    db.delete(zone)
    db.commit()
    return None