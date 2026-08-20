from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.api.auth import get_current_user
from app.services.permission_service import has_permission
from datetime import datetime, timedelta

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/orders-by-day")
def orders_by_day(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "view_statistics"):
        raise HTTPException(status_code=403, detail="Permission manquante : voir les statistiques")
    since = datetime.utcnow() - timedelta(days=7)
    orders = db.query(
        func.date(Order.created_at).label('day'),
        func.count(Order.id).label('count')
    ).filter(
        Order.tenant_id == current_user.tenant_id,
        Order.created_at >= since
    ).group_by(func.date(Order.created_at)).all()

    result = []
    for day, count in orders:
        result.append({"day": str(day), "orders": count})
    return result

@router.get("/top-products")
def top_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "view_statistics"):
        raise HTTPException(status_code=403, detail="Permission manquante : voir les statistiques")
    items = db.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_qty')
    ).join(
        OrderItem, OrderItem.product_id == Product.id
    ).join(
        Order, Order.id == OrderItem.order_id
    ).filter(
        Order.tenant_id == current_user.tenant_id
    ).group_by(
        Product.name
    ).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(5).all()

    result = [{"product": name, "quantity": total_qty} for name, total_qty in items]
    return result

@router.get("/revenue")
def revenue(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "view_statistics"):
        raise HTTPException(status_code=403, detail="Permission manquante : voir les statistiques")
    total = db.query(func.sum(Order.total_amount)).filter(
        Order.tenant_id == current_user.tenant_id,
        Order.status.notin_(["CANCELLED", "REFUSED", "EXPIRED"])
    ).scalar() or 0
    return {"total_revenue_cents": total}