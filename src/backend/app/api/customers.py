from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.models.customer import Customer
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.conversation import Conversation
from app.models.message_metadata import MessageMetadata
from app.models.time_slot import TimeSlot
from app.models.product import Product
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.api.auth import get_current_user
from app.services.permission_service import has_permission

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("", response_model=List[CustomerRead])
def list_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customers = db.query(Customer).filter(Customer.tenant_id == current_user.tenant_id).all()
    return customers

@router.post("", response_model=CustomerRead, status_code=201)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_customers"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les clients")

    existing = db.query(Customer).filter(
        Customer.tenant_id == current_user.tenant_id,
        Customer.signal_phone_hash == customer_data.signal_phone_hash
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Un client avec ce hash existe déjà")

    customer = Customer(
        tenant_id=current_user.tenant_id,
        signal_phone_hash=customer_data.signal_phone_hash
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.patch("/{customer_id}", response_model=CustomerRead)
def update_customer(
    customer_id: UUID,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_customers"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les clients")

    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.tenant_id == current_user.tenant_id
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")

    if customer_data.signal_phone_hash is not None:
        existing = db.query(Customer).filter(
            Customer.tenant_id == current_user.tenant_id,
            Customer.signal_phone_hash == customer_data.signal_phone_hash,
            Customer.id != customer.id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Un client avec ce hash existe déjà")
        customer.signal_phone_hash = customer_data.signal_phone_hash

    db.commit()
    db.refresh(customer)
    return customer

@router.delete("/{customer_id}", status_code=204)
def delete_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_customers"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les clients")

    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.tenant_id == current_user.tenant_id
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")

    # Libérer créneaux et stock des commandes
    orders = db.query(Order).filter(Order.customer_id == customer_id).all()
    for order in orders:
        if order.scheduled_slot_id:
            slot = db.query(TimeSlot).filter(TimeSlot.id == order.scheduled_slot_id).first()
            if slot and slot.booked_count > 0:
                slot.booked_count -= 1
                db.add(slot)
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        for item in order_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product and product.stock_mode == "limited":
                if product.stock_quantity is not None:
                    product.stock_quantity += item.quantity
                    db.add(product)
        db.query(OrderItem).filter(OrderItem.order_id == order.id).delete()
    db.query(Order).filter(Order.customer_id == customer_id).delete()

    # Paniers et articles
    carts = db.query(Cart).filter(Cart.customer_id == customer_id).all()
    for cart in carts:
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.query(Cart).filter(Cart.customer_id == customer_id).delete()

    # Conversations et messages
    conversations = db.query(Conversation).filter(Conversation.customer_id == customer_id).all()
    for conv in conversations:
        db.query(MessageMetadata).filter(MessageMetadata.conversation_id == conv.id).delete()
    db.query(Conversation).filter(Conversation.customer_id == customer_id).delete()

    db.delete(customer)
    db.commit()
    return None