from sqlalchemy.orm import Session
from typing import List
from app.models.product import Product
from app.models.category import Category
from app.models.variant import Variant

def list_products(db: Session, tenant_id) -> List[Product]:
    """Retourne la liste des produits actifs du tenant."""
    products = db.query(Product).filter(
        Product.tenant_id == tenant_id,
        Product.active == True
    ).all()
    return products

def get_product(db: Session, tenant_id, product_id) -> Product:
    """Retourne un produit par ID."""
    product = db.query(Product).filter(
        Product.tenant_id == tenant_id,
        Product.id == product_id,
        Product.active == True
    ).first()
    return product

def list_categories(db: Session, tenant_id) -> List[Category]:
    """Retourne les catégories actives."""
    categories = db.query(Category).filter(
        Category.tenant_id == tenant_id,
        Category.active == True
    ).all()
    return categories