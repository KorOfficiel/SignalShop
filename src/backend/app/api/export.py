from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from io import StringIO
import csv
from app.db.database import get_db
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.api.auth import get_current_user
from app.services.permission_service import has_permission

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/orders")
def export_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "export_orders"):
        raise HTTPException(status_code=403, detail="Permission manquante : exporter les commandes")

    orders = db.query(Order).filter(Order.tenant_id == current_user.tenant_id).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID commande", "Client ID", "Statut", "Total (€)", "Frais livraison (€)", "Date", "Produits", "Quantités"])

    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        product_details = []
        quantities = []
        for item in items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            product_name = product.name if product else "Produit supprimé"
            product_details.append(f"{product_name} (x{item.quantity})")
            quantities.append(str(item.quantity))

        writer.writerow([
            str(order.id),
            str(order.customer_id),
            order.status,
            f"{order.total_amount / 100:.2f}",
            f"{order.delivery_fee / 100:.2f}",
            order.created_at.strftime("%Y-%m-%d %H:%M"),
            "; ".join(product_details),
            "; ".join(quantities),
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=commandes.csv"}
    )