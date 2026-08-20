from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.api.auth import get_current_user
from app.core.security import get_password_hash
from app.services.permission_service import has_permission

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_users"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les utilisateurs")
    users = db.query(User).filter(User.tenant_id == current_user.tenant_id).all()
    return users

@router.post("", response_model=UserRead, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_users"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les utilisateurs")

    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Un utilisateur avec cet email existe déjà")

    new_user = User(
        tenant_id=current_user.tenant_id,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_users"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les utilisateurs")

    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == current_user.tenant_id
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if user_data.email is not None:
        existing = db.query(User).filter(User.email == user_data.email, User.id != user.id).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email déjà utilisé")
        user.email = user_data.email
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.role is not None:
        if user.id == current_user.id and user_data.role != "OWNER":
            owners_count = db.query(User).filter(
                User.tenant_id == current_user.tenant_id,
                User.role == "OWNER",
                User.id != user.id
            ).count()
            if owners_count == 0:
                raise HTTPException(status_code=400, detail="Impossible de retirer votre rôle OWNER")
        user.role = user_data.role
    if user_data.password is not None:
        user.hashed_password = get_password_hash(user_data.password)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_users"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les utilisateurs")

    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas supprimer votre propre compte")

    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == current_user.tenant_id
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if user.role == "OWNER":
        owners_count = db.query(User).filter(
            User.tenant_id == current_user.tenant_id,
            User.role == "OWNER"
        ).count()
        if owners_count <= 1:
            raise HTTPException(status_code=400, detail="Impossible de supprimer le dernier OWNER")

    db.delete(user)
    db.commit()
    return None