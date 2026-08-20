from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

from app.models.product import Product
from app.models.category import Category
from app.models.variant import Variant
from app.models.customer import Customer
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem

# ========== FONCTIONS INTERNES ==========

def _get_or_create_cart(db: Session, tenant_id, customer_id) -> Cart:
    """Récupère le panier actif du client ou en crée un."""
    cart = db.query(Cart).filter(
        Cart.tenant_id == tenant_id,
        Cart.customer_id == customer_id,
        Cart.status == "ACTIVE"
    ).first()
    if not cart:
        cart = Cart(
            tenant_id=tenant_id,
            customer_id=customer_id,
            status="ACTIVE"
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

# ========== OUTILS EXPOSÉS ==========

def get_catalog(db: Session, tenant_id, active_only: bool = True) -> List[Dict[str, Any]]:
    """Retourne les produits actifs sous forme de dictionnaires simples."""
    query = db.query(Product).filter(Product.tenant_id == tenant_id)
    if active_only:
        query = query.filter(Product.active == True)
    products = query.all()
    result = []
    for p in products:
        result.append({
            "id": str(p.id),
            "name": p.name,
            "description": p.description,
            "base_price": p.base_price,
            "unit": p.unit,
            "stock_mode": p.stock_mode,
            "stock_quantity": p.stock_quantity,
            "active": p.active
        })
    return result

def get_product_detail(db: Session, tenant_id, product_id: UUID) -> Optional[Dict[str, Any]]:
    """Retourne les détails d'un produit avec ses variantes et options."""
    product = db.query(Product).filter(
        Product.tenant_id == tenant_id,
        Product.id == product_id
    ).first()
    if not product:
        return None

    variants = db.query(Variant).filter(Variant.product_id == product_id).all()
    options = db.query(OptionDefinition).filter(OptionDefinition.product_id == product_id).all() if False else []

    return {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "base_price": product.base_price,
        "unit": product.unit,
        "stock_mode": product.stock_mode,
        "stock_quantity": product.stock_quantity,
        "variants": [
            {
                "id": str(v.id),
                "name": v.name,
                "price_modifier": v.price_modifier,
                "price_override": v.price_override,
                "stock_quantity": v.stock_quantity
            }
            for v in variants
        ]
    }

def check_stock(db: Session, tenant_id, product_id: UUID, quantity: int) -> Dict[str, Any]:
    """Vérifie la disponibilité du produit."""
    product = db.query(Product).filter(
        Product.tenant_id == tenant_id,
        Product.id == product_id
    ).first()
    if not product:
        return {"available": False, "message": "Produit introuvable"}

    if product.stock_mode == "illimited":
        return {"available": True, "message": "Stock illimité"}

    if product.stock_mode == "unavailable":
        return {"available": False, "message": "Produit indisponible"}

    if product.stock_quantity is None:
        return {"available": False, "message": "Stock non défini"}

    if product.stock_quantity >= quantity:
        return {"available": True, "message": f"Stock disponible : {product.stock_quantity}"}
    else:
        return {"available": False, "message": f"Stock insuffisant : {product.stock_quantity}"}

def add_to_cart(
    db: Session,
    tenant_id,
    customer_id: UUID,
    product_id: UUID,
    quantity: int = 1,
    variant_id: Optional[UUID] = None
) -> CartItem:
    """Ajoute un article au panier du client."""
    cart = _get_or_create_cart(db, tenant_id, customer_id)

    product = db.query(Product).filter(
        Product.tenant_id == tenant_id,
        Product.id == product_id,
        Product.active == True
    ).first()
    if not product:
        raise ValueError("Produit introuvable ou inactif")

    unit_price = product.base_price
    if variant_id:
        variant = db.query(Variant).filter(Variant.id == variant_id).first()
        if not variant:
            raise ValueError("Variante introuvable")
        if variant.price_override is not None:
            unit_price = variant.price_override
        else:
            unit_price += variant.price_modifier

    # Vérifier le stock si limité
    if product.stock_mode == "limited":
        if product.stock_quantity is None or product.stock_quantity < quantity:
            raise ValueError("Stock insuffisant")

    total_price = unit_price * quantity

    item = CartItem(
        cart_id=cart.id,
        product_id=product_id,
        variant_id=variant_id,
        quantity=quantity,
        options=None,
        unit_price=unit_price,
        total_price=total_price
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def create_order_from_cart(db: Session, tenant_id, cart_id: UUID) -> Order:
    """Crée une commande à partir d'un panier, avec décrémentation du stock."""
    cart = db.query(Cart).filter(
        Cart.tenant_id == tenant_id,
        Cart.id == cart_id
    ).first()
    if not cart:
        raise ValueError("Panier introuvable")

    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not cart_items:
        raise ValueError("Le panier est vide")

    total_amount = sum(item.total_price for item in cart_items)
    # Pas de frais de livraison pour l'instant
    delivery_fee = 0
    total_amount += delivery_fee

    # Vérification du stock et décrémentation
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product.stock_mode == "limited":
            if product.stock_quantity is None or product.stock_quantity < item.quantity:
                raise ValueError(f"Stock insuffisant pour {product.name}")
            product.stock_quantity -= item.quantity
            db.add(product)

    order = Order(
        tenant_id=tenant_id,
        customer_id=cart.customer_id,
        status="CONFIRMED",
        total_amount=total_amount,
        delivery_fee=delivery_fee,
        delivery_zone_id=None,
        delivery_address=None,
        delivery_instructions=None,
        scheduled_slot_id=None,
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
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, tenant_id, order_id: UUID) -> Optional[Order]:
    """Retourne une commande."""
    return db.query(Order).filter(
        Order.tenant_id == tenant_id,
        Order.id == order_id
    ).first()