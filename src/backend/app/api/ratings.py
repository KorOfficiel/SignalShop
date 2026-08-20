from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, RatingRead
from app.api.auth import get_current_user
from app.services.permission_service import has_permission

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.get("", response_model=List[RatingRead])
def list_ratings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ratings = db.query(Rating).filter(Rating.tenant_id == current_user.tenant_id).all()
    return ratings

@router.post("", response_model=RatingRead, status_code=201)
def create_rating(
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_ratings"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les évaluations")
    if rating_data.rating < 1 or rating_data.rating > 5:
        raise HTTPException(status_code=422, detail="La note doit être entre 1 et 5")
    rating = Rating(
        tenant_id=current_user.tenant_id,
        customer_id=rating_data.customer_id,
        rating=rating_data.rating,
        comment=rating_data.comment
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating

@router.delete("/{rating_id}", status_code=204)
def delete_rating(
    rating_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_ratings"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les évaluations")
    rating = db.query(Rating).filter(
        Rating.id == rating_id,
        Rating.tenant_id == current_user.tenant_id
    ).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Évaluation introuvable")
    db.delete(rating)
    db.commit()
    return None