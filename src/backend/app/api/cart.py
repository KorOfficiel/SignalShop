from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.variant import Variant
from app.schemas.cart import CartCreate, CartRead
from app.schemas.cart_item import CartItemCreate, CartItemUpdate, CartItemRead
from app.api.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

def require_role(user: User, allowed_roles: list):
    if user.role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissions insuffisantes")

@router.post("", response_model=CartRead, status_code=201)
def create_cart(
    cart_data: CartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée un nouveau panier pour un client."""
    # Vérifier que le client appartient au même tenant que l'utilisateur
    from app.models.customer import Customer
    customer = db.query(Customer).filter(
        Customer.id == cart_data.customer_id,
        Customer.tenant_id == current_user.tenant_id
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")

    cart = Cart(
        tenant_id=current_user.tenant_id,
        customer_id=cart_data.customer_id,
        status=cart_data.status
    )
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

@router.get("/{cart_id}", response_model=CartRead)
def get_cart(
    cart_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.tenant_id == current_user.tenant_id
    ).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Panier introuvable")
    return cart

@router.post("/{cart_id}/items", response_model=CartItemRead, status_code=201)
def add_item_to_cart(
    cart_id: UUID,
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ajoute un article au panier."""
    cart = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.tenant_id == current_user.tenant_id
    ).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Panier introuvable")

    # Vérifier que le produit existe et est actif
    product = db.query(Product).filter(
        Product.id == item_data.product_id,
        Product.tenant_id == current_user.tenant_id,
        Product.active == True
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable ou inactif")

    # Calcul du prix unitaire (plus tard via service de tarification, pour l'instant on le fait simple)
    unit_price = product.base_price
    if item_data.variant_id:
        variant = db.query(Variant).filter(Variant.id == item_data.variant_id).first()
        if not variant:
            raise HTTPException(status_code=404, detail="Variante introuvable")
        if variant.price_override is not None:
            unit_price = variant.price_override
        else:
            unit_price += variant.price_modifier

    # Vérifier le stock (simple, sans atomicité pour l'instant, on améliorera plus tard)
    if product.stock_mode == "limited":
        if product.stock_quantity is None or product.stock_quantity < item_data.quantity:
            raise HTTPException(status_code=409, detail="Stock insuffisant")
        # Ne pas décrémenter ici, seulement à la commande

    total_price = unit_price * item_data.quantity

    item = CartItem(
        cart_id=cart_id,
        product_id=item_data.product_id,
        variant_id=item_data.variant_id,
        quantity=item_data.quantity,
        options=item_data.options,
        unit_price=unit_price,
        total_price=total_price
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.patch("/{cart_id}/items/{item_id}", response_model=CartItemRead)
def update_cart_item(
    cart_id: UUID,
    item_id: UUID,
    item_data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.tenant_id == current_user.tenant_id
    ).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Panier introuvable")

    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Article introuvable")

    # Mise à jour des champs
    if item_data.quantity is not None:
        item.quantity = item_data.quantity
    if item_data.variant_id is not None:
        # Recalculer le prix si la variante change
        product = db.query(Product).filter(Product.id == item.product_id).first()
        unit_price = product.base_price
        variant = db.query(Variant).filter(Variant.id == item_data.variant_id).first()
        if variant:
            if variant.price_override is not None:
                unit_price = variant.price_override
            else:
                unit_price += variant.price_modifier
        item.variant_id = item_data.variant_id
        item.unit_price = unit_price
    if item_data.options is not None:
        item.options = item_data.options

    # Recalculer le total
    if item_data.quantity is not None or item_data.variant_id is not None:
        item.total_price = item.unit_price * item.quantity

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{cart_id}/items/{item_id}", status_code=204)
def remove_cart_item(
    cart_id: UUID,
    item_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.tenant_id == current_user.tenant_id
    ).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Panier introuvable")

    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Article introuvable")

    db.delete(item)
    db.commit()
    return None