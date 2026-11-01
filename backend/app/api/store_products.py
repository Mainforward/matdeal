from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import Product, Store, StoreProduct
from app.schemas.product import (
    StoreProductCreate,
    StoreProductResponse,
)

router = APIRouter(
    prefix="/store-products",
    tags=["store-products"],
)


@router.post(
    "",
    response_model=StoreProductResponse,
    status_code=201,
)
def create_store_product(
    data: StoreProductCreate,
    db: Session = Depends(get_db),
):
    store = (
        db.query(Store)
        .filter(Store.id == data.store_id)
        .first()
    )

    if store is None:
        raise HTTPException(
            status_code=404,
            detail="Store not found",
        )

    product = (
        db.query(Product)
        .filter(Product.id == data.product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    existing = (
        db.query(StoreProduct)
        .filter(
            StoreProduct.store_id == data.store_id,
            StoreProduct.external_id == data.external_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Store product with this external_id already exists",
        )

    store_product = StoreProduct(
        store_id=data.store_id,
        product_id=data.product_id,
        external_id=data.external_id,
        external_name=data.external_name,
        external_url=data.external_url,
        available=data.available,
    )

    db.add(store_product)
    db.commit()
    db.refresh(store_product)

    return StoreProductResponse(
        id=store_product.id,
        store_id=store_product.store_id,
        product_id=store_product.product_id,
        external_id=store_product.external_id,
        external_name=store_product.external_name,
        external_url=store_product.external_url,
        available=store_product.available,
    )