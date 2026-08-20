from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.variant import Variant
from app.models.option_definition import OptionDefinition
from app.models.cart_item import CartItem
from app.models.order_item import OrderItem
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.schemas.variant import VariantCreate, VariantRead, VariantUpdate
from app.schemas.option_definition import OptionDefinitionCreate, OptionDefinitionRead, OptionDefinitionUpdate
from app.api.auth import get_current_user
from app.services.notification_service import create_notification
from app.services.permission_service import has_permission
from app.services.audit_service import log_audit

router = APIRouter(prefix="/catalog", tags=["catalog"])

# ========== Catégories ==========

@router.post("/categories", response_model=CategoryRead, status_code=201)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_categories"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les catégories")
    category = Category(
        tenant_id=current_user.tenant_id,
        **category_data.dict()
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    log_audit(db, current_user, "create_category", "category", str(category.id), {"name": category.name})
    db.commit()
    return category

@router.get("/categories", response_model=List[CategoryRead])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = db.query(Category).filter(Category.tenant_id == current_user.tenant_id).all()
    return categories

@router.get("/categories/{category_id}", response_model=CategoryRead)
def get_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.tenant_id == current_user.tenant_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return category

@router.patch("/categories/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_categories"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les catégories")
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.tenant_id == current_user.tenant_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    for field, value in category_data.dict(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    log_audit(db, current_user, "update_category", "category", str(category.id), {"name": category.name})
    db.commit()
    return category

@router.delete("/categories/{category_id}", status_code=204)
def delete_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_categories"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les catégories")
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.tenant_id == current_user.tenant_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")

    linked_products = db.query(Product).filter(Product.category_id == category_id).count()
    if linked_products > 0:
        raise HTTPException(
            status_code=409,
            detail="Impossible de supprimer cette catégorie car des produits y sont liés."
        )

    db.delete(category)
    log_audit(db, current_user, "delete_category", "category", str(category_id))
    db.commit()
    return None

# ========== Produits ==========

@router.post("/products", response_model=ProductRead, status_code=201)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_products"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les produits")

    if product_data.category_id:
        category = db.query(Category).filter(
            Category.id == product_data.category_id,
            Category.tenant_id == current_user.tenant_id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Catégorie introuvable")

    product = Product(
        tenant_id=current_user.tenant_id,
        **product_data.dict()
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    log_audit(db, current_user, "create_product", "product", str(product.id), {"name": product.name, "price": product.base_price})
    db.commit()
    return product

@router.get("/products", response_model=List[ProductRead])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = db.query(Product).filter(Product.tenant_id == current_user.tenant_id).all()
    return products

@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return product

@router.patch("/products/{product_id}", response_model=ProductRead)
def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_products"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les produits")
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    if product_data.category_id is not None:
        category = db.query(Category).filter(
            Category.id == product_data.category_id,
            Category.tenant_id == current_user.tenant_id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Catégorie introuvable")

    for field, value in product_data.dict(exclude_unset=True).items():
        setattr(product, field, value)

    if product.stock_mode == "limited" and product.stock_quantity is not None and product.alert_threshold is not None:
        if product.stock_quantity < product.alert_threshold:
            create_notification(
                db=db,
                tenant_id=current_user.tenant_id,
                type="stock_low",
                message=f"Stock faible pour {product.name} : {product.stock_quantity} restant"
            )

    db.commit()
    db.refresh(product)
    log_audit(db, current_user, "update_product", "product", str(product.id), {"name": product.name})
    db.commit()
    return product

@router.delete("/products/{product_id}", status_code=204)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_products"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les produits")
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    order_items = db.query(OrderItem).filter(OrderItem.product_id == product_id).count()
    if order_items > 0:
        raise HTTPException(
            status_code=409,
            detail="Impossible de supprimer ce produit car il est lié à des commandes."
        )

    db.query(Variant).filter(Variant.product_id == product_id).delete()
    db.query(OptionDefinition).filter(OptionDefinition.product_id == product_id).delete()
    db.query(CartItem).filter(CartItem.product_id == product_id).delete()

    db.delete(product)
    log_audit(db, current_user, "delete_product", "product", str(product_id))
    db.commit()
    return None

# ========== Variantes ==========

@router.post("/variants", response_model=VariantRead, status_code=201)
def create_variant(
    variant_data: VariantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_products"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les produits")
    product = db.query(Product).filter(
        Product.id == variant_data.product_id,
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    variant = Variant(**variant_data.dict())
    db.add(variant)
    db.commit()
    db.refresh(variant)
    log_audit(db, current_user, "create_variant", "variant", str(variant.id), {"name": variant.name})
    db.commit()
    return variant

@router.get("/variants", response_model=List[VariantRead])
def list_variants(
    product_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Variant).join(Product).filter(Product.tenant_id == current_user.tenant_id)
    if product_id:
        query = query.filter(Variant.product_id == product_id)
    return query.all()

@router.patch("/variants/{variant_id}", response_model=VariantRead)
def update_variant(
    variant_id: UUID,
    variant_data: VariantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_products"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les produits")
    variant = db.query(Variant).filter(Variant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variante introuvable")
    for field, value in variant_data.dict(exclude_unset=True).items():
        setattr(variant, field, value)
    db.commit()
    db.refresh(variant)
    log_audit(db, current_user, "update_variant", "variant", str(variant.id), {"name": variant.name})
    db.commit()
    return variant

@router.delete("/variants/{variant_id}", status_code=204)
def delete_variant(
    variant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_products"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les produits")
    variant = db.query(Variant).filter(Variant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variante introuvable")
    db.delete(variant)
    log_audit(db, current_user, "delete_variant", "variant", str(variant_id))
    db.commit()
    return None

# ========== Options ==========

@router.post("/options", response_model=OptionDefinitionRead, status_code=201)
def create_option(
    option_data: OptionDefinitionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_products"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les produits")
    product = db.query(Product).filter(
        Product.id == option_data.product_id,
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    option = OptionDefinition(**option_data.dict())
    db.add(option)
    db.commit()
    db.refresh(option)
    log_audit(db, current_user, "create_option", "option", str(option.id), {"name": option.name})
    db.commit()
    return option

@router.get("/options", response_model=List[OptionDefinitionRead])
def list_options(
    product_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(OptionDefinition).join(Product).filter(Product.tenant_id == current_user.tenant_id)
    if product_id:
        query = query.filter(OptionDefinition.product_id == product_id)
    return query.all()

@router.patch("/options/{option_id}", response_model=OptionDefinitionRead)
def update_option(
    option_id: UUID,
    option_data: OptionDefinitionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_products"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les produits")
    option = db.query(OptionDefinition).filter(OptionDefinition.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option introuvable")
    for field, value in option_data.dict(exclude_unset=True).items():
        setattr(option, field, value)
    db.commit()
    db.refresh(option)
    log_audit(db, current_user, "update_option", "option", str(option.id), {"name": option.name})
    db.commit()
    return option

@router.delete("/options/{option_id}", status_code=204)
def delete_option(
    option_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "manage_products"):
        raise HTTPException(status_code=403, detail="Permission manquante : gérer les produits")
    option = db.query(OptionDefinition).filter(OptionDefinition.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option introuvable")
    db.delete(option)
    log_audit(db, current_user, "delete_option", "option", str(option_id))
    db.commit()
    return None