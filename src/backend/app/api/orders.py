from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
import json

from app.db.database import get_db
from app.models.user import User
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.variant import Variant
from app.models.time_slot import TimeSlot
from app.models.delivery_zone import DeliveryZone
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate
from app.api.auth import get_current_user
from app.services.notification_service import create_notification
from app.services.permission_service import has_permission
from app.services.audit_service import log_audit
from app.services.crypto_service import encrypt_data, decrypt_data

router = APIRouter(prefix="/orders", tags=["orders"])

# Schémas pour création directe
class DirectOrderItem(BaseModel):
    product_id: UUID
    variant_id: Optional[UUID] = None
    quantity: int = 1
    options: Optional[Dict[str, Any]] = None

class DirectOrderCreate(BaseModel):
    customer_id: UUID
    items: List[DirectOrderItem]
    delivery_zone_id: Optional[UUID] = None
    delivery_address: Optional[Dict[str, Any]] = None
    delivery_instructions: Optional[str] = None
    scheduled_slot_id: Optional[UUID] = None
    status: str = "CONFIRMED"

def decrypt_order(order: Order):
    """Déchiffre les champs sensibles d'une commande."""
    if order.delivery_address:
        try:
            order.delivery_address = json.loads(decrypt_data(order.delivery_address))
        except:
            pass
    if order.delivery_instructions:
        try:
            order.delivery_instructions = decrypt_data(order.delivery_instructions)
        except:
            pass
    return order

# ========== CRÉATION DEPUIS PANIER ==========

@router.post("", response_model=OrderRead, status_code=201)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_orders"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les commandes")

    if not order_data.cart_id:
        raise HTTPException(status_code=400, detail="cart_id est requis")

    cart = db.query(Cart).filter(
        Cart.id == order_data.cart_id,
        Cart.tenant_id == current_user.tenant_id,
        Cart.status == "ACTIVE"
    ).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Panier introuvable ou inactif")

    customer_id = cart.customer_id
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Le panier est vide")

    if order_data.scheduled_slot_id:
        slot = db.query(TimeSlot).filter(
            TimeSlot.id == order_data.scheduled_slot_id,
            TimeSlot.tenant_id == current_user.tenant_id,
            TimeSlot.active == True
        ).with_for_update().first()
        if not slot:
            raise HTTPException(status_code=404, detail="Créneau introuvable")
        if slot.booked_count >= slot.capacity:
            raise HTTPException(status_code=409, detail="Créneau complet")
        slot.booked_count += 1
        db.add(slot)

    total_amount = sum(item.total_price for item in cart_items)
    delivery_fee = 0
    if order_data.delivery_zone_id:
        zone = db.query(DeliveryZone).filter(
            DeliveryZone.id == order_data.delivery_zone_id,
            DeliveryZone.tenant_id == current_user.tenant_id
        ).first()
        if not zone:
            raise HTTPException(status_code=404, detail="Zone de livraison introuvable")
        delivery_fee = zone.fee
        total_amount += delivery_fee

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
        if not product:
            raise HTTPException(status_code=404, detail="Produit introuvable")
        if product.stock_mode == "limited":
            if product.stock_quantity is None or product.stock_quantity < item.quantity:
                raise HTTPException(status_code=409, detail=f"Stock insuffisant pour {product.name}")
            product.stock_quantity -= item.quantity
            db.add(product)

    # Chiffrer les données sensibles
    encrypted_address = encrypt_data(json.dumps(order_data.delivery_address)) if order_data.delivery_address else None
    encrypted_instructions = encrypt_data(order_data.delivery_instructions) if order_data.delivery_instructions else None

    order = Order(
        tenant_id=current_user.tenant_id,
        customer_id=customer_id,
        status="CONFIRMED",
        total_amount=total_amount,
        delivery_fee=delivery_fee,
        delivery_zone_id=order_data.delivery_zone_id,
        delivery_address=encrypted_address,
        delivery_instructions=encrypted_instructions,
        scheduled_slot_id=order_data.scheduled_slot_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(order)
    db.flush()

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            variant_id=item.variant_id,
            quantity=item.quantity,
            options=item.options,
            unit_price=item.unit_price,
            total_price=item.total_price
        )
        db.add(order_item)
        db.delete(item)

    cart.status = "INACTIVE"
    db.add(cart)

    create_notification(
        db=db,
        tenant_id=current_user.tenant_id,
        type="order_created",
        message=f"Nouvelle commande #{order.id} de {order.total_amount/100:.2f} €"
    )
    log_audit(db, current_user, "create_order", "order", str(order.id))

    db.commit()
    db.refresh(order)
    decrypt_order(order)
    return order

# ========== CRÉATION DIRECTE ==========

@router.post("/direct", response_model=OrderRead, status_code=201)
def create_direct_order(
    order_data: DirectOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_orders"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les commandes")

    from app.models.customer import Customer
    customer = db.query(Customer).filter(
        Customer.id == order_data.customer_id,
        Customer.tenant_id == current_user.tenant_id
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")

    if not order_data.items:
        raise HTTPException(status_code=400, detail="Aucun article")

    total_amount = 0
    prepared_items = []
    for item_data in order_data.items:
        product = db.query(Product).filter(
            Product.id == item_data.product_id,
            Product.tenant_id == current_user.tenant_id,
            Product.active == True
        ).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produit {item_data.product_id} introuvable")

        unit_price = product.base_price
        if item_data.variant_id:
            variant = db.query(Variant).filter(Variant.id == item_data.variant_id).first()
            if not variant:
                raise HTTPException(status_code=404, detail="Variante introuvable")
            if variant.price_override is not None:
                unit_price = variant.price_override
            else:
                unit_price += variant.price_modifier

        total_amount += unit_price * item_data.quantity
        prepared_items.append({
            "product": product,
            "variant_id": item_data.variant_id,
            "quantity": item_data.quantity,
            "options": item_data.options,
            "unit_price": unit_price
        })

    delivery_fee = 0
    if order_data.delivery_zone_id:
        zone = db.query(DeliveryZone).filter(
            DeliveryZone.id == order_data.delivery_zone_id,
            DeliveryZone.tenant_id == current_user.tenant_id
        ).first()
        if not zone:
            raise HTTPException(status_code=404, detail="Zone de livraison introuvable")
        delivery_fee = zone.fee
        total_amount += delivery_fee

    if order_data.scheduled_slot_id:
        slot = db.query(TimeSlot).filter(
            TimeSlot.id == order_data.scheduled_slot_id,
            TimeSlot.tenant_id == current_user.tenant_id,
            TimeSlot.active == True
        ).with_for_update().first()
        if not slot:
            raise HTTPException(status_code=404, detail="Créneau introuvable")
        if slot.booked_count >= slot.capacity:
            raise HTTPException(status_code=409, detail="Créneau complet")
        slot.booked_count += 1
        db.add(slot)

    encrypted_address = encrypt_data(json.dumps(order_data.delivery_address)) if order_data.delivery_address else None
    encrypted_instructions = encrypt_data(order_data.delivery_instructions) if order_data.delivery_instructions else None

    order = Order(
        tenant_id=current_user.tenant_id,
        customer_id=customer.id,
        status=order_data.status,
        total_amount=total_amount,
        delivery_fee=delivery_fee,
        delivery_zone_id=order_data.delivery_zone_id,
        delivery_address=encrypted_address,
        delivery_instructions=encrypted_instructions,
        scheduled_slot_id=order_data.scheduled_slot_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(order)
    db.flush()

    for item in prepared_items:
        product = item["product"]
        if product.stock_mode == "limited":
            if product.stock_quantity is None or product.stock_quantity < item["quantity"]:
                raise HTTPException(status_code=409, detail=f"Stock insuffisant pour {product.name}")
            product.stock_quantity -= item["quantity"]
            db.add(product)

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            variant_id=item["variant_id"],
            quantity=item["quantity"],
            options=item["options"],
            unit_price=item["unit_price"],
            total_price=item["unit_price"] * item["quantity"]
        )
        db.add(order_item)

    create_notification(
        db=db,
        tenant_id=current_user.tenant_id,
        type="order_created",
        message=f"Nouvelle commande #{order.id} de {order.total_amount/100:.2f} €"
    )
    log_audit(db, current_user, "create_direct_order", "order", str(order.id))

    db.commit()
    db.refresh(order)
    decrypt_order(order)
    return order

# ========== LISTE ET DÉTAIL ==========

@router.get("", response_model=List[OrderRead])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.tenant_id == current_user.tenant_id).all()
    for order in orders:
        decrypt_order(order)
    return orders

@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.tenant_id == current_user.tenant_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    decrypt_order(order)
    return order

# ========== MODIFICATION ==========

@router.patch("/{order_id}", response_model=OrderRead)
def update_order(
    order_id: UUID,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_orders"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les commandes")

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.tenant_id == current_user.tenant_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")

    if order_data.status is not None:
        old_status = order.status
        order.status = order_data.status
        if old_status != "CANCELLED" and order_data.status == "CANCELLED":
            _release_stock_and_slot(db, order)

    if order_data.delivery_address is not None:
        order.delivery_address = encrypt_data(json.dumps(order_data.delivery_address))
    if order_data.delivery_instructions is not None:
        order.delivery_instructions = encrypt_data(order_data.delivery_instructions)
    if order_data.scheduled_slot_id is not None:
        slot = db.query(TimeSlot).filter(
            TimeSlot.id == order_data.scheduled_slot_id,
            TimeSlot.tenant_id == current_user.tenant_id,
            TimeSlot.active == True
        ).first()
        if not slot:
            raise HTTPException(status_code=404, detail="Créneau introuvable")
        if order.scheduled_slot_id and order.scheduled_slot_id != order_data.scheduled_slot_id:
            old_slot = db.query(TimeSlot).filter(TimeSlot.id == order.scheduled_slot_id).first()
            if old_slot and old_slot.booked_count > 0:
                old_slot.booked_count -= 1
                db.add(old_slot)
        if order.scheduled_slot_id != order_data.scheduled_slot_id:
            slot.booked_count += 1
            db.add(slot)
        order.scheduled_slot_id = order_data.scheduled_slot_id

    order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    decrypt_order(order)
    return order

# ========== ANNULATION ==========

@router.post("/{order_id}/cancel", response_model=OrderRead)
def cancel_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_orders"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les commandes")

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.tenant_id == current_user.tenant_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")

    if order.status in ["COMPLETED", "CANCELLED"]:
        raise HTTPException(status_code=409, detail="Commande déjà terminée ou annulée")

    _release_stock_and_slot(db, order)
    order.status = "CANCELLED"
    order.updated_at = datetime.utcnow()

    create_notification(
        db=db,
        tenant_id=current_user.tenant_id,
        type="order_cancelled",
        message=f"Commande #{order.id} annulée"
    )
    log_audit(db, current_user, "cancel_order", "order", str(order.id))

    db.commit()
    db.refresh(order)
    decrypt_order(order)
    return order

# ========== SUPPRESSION ==========

@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_orders"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les commandes")

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.tenant_id == current_user.tenant_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")

    if order.scheduled_slot_id:
        slot = db.query(TimeSlot).filter(TimeSlot.id == order.scheduled_slot_id).first()
        if slot and slot.booked_count > 0:
            slot.booked_count -= 1
            db.add(slot)

    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product and product.stock_mode == "limited":
            if product.stock_quantity is not None:
                product.stock_quantity += item.quantity
                db.add(product)

    db.query(OrderItem).filter(OrderItem.order_id == order.id).delete()
    db.delete(order)

    create_notification(
        db=db,
        tenant_id=current_user.tenant_id,
        type="order_deleted",
        message=f"Commande #{order.id} supprimée"
    )
    log_audit(db, current_user, "delete_order", "order", str(order_id))

    db.commit()
    return None

# ========== FONCTION UTILITAIRE ==========

def _release_stock_and_slot(db: Session, order: Order):
    if order.scheduled_slot_id:
        slot = db.query(TimeSlot).filter(TimeSlot.id == order.scheduled_slot_id).first()
        if slot and slot.booked_count > 0:
            slot.booked_count -= 1
            db.add(slot)

    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product and product.stock_mode == "limited":
            if product.stock_quantity is not None:
                product.stock_quantity += item.quantity
                db.add(product)