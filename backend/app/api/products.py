from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.product import Product
from app.models.store_product import StoreProduct
from app.models.store import Store
from app.models.price_history import PriceHistory

from app.schemas.product import (
    ProductOffersResponse,
    ProductResponse,
)

from uuid import UUID

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get(
     "",
    response_model=list[ProductResponse]
)

def search_products(
    search: str | None = Query(
        default=None,
        min_length=1,
    ),
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            Product.name.ilike(search_pattern)
            | Product.brand.ilike(search_pattern)
        )

    return query.order_by(Product.name).limit(50).all()



@router.get(
    "/{product_id}/offers",
    response_model=ProductOffersResponse    
)



def get_product_offers(
    product_id: UUID,
    db: Session = Depends(get_db),
):

    product = db.query(Product).filter(Product.id == product_id).first()

    #print("PRODUCT ID:", product_id)
    #print("PRODUCTS:", db.query(Product).all())

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )
    
    latest_price = (
        db.query(
            PriceHistory.store_product_id,
            func.max(PriceHistory.captured_at).label("latest_captured_at"),
        )
        .group_by(PriceHistory.store_product_id)
        .subquery()
    )

    results = (
        db.query(
            Store.store_name,
            Store.chain_name,
            PriceHistory.price,
            PriceHistory.currency,
        )
        .join(
            StoreProduct,
            StoreProduct.store_id == Store.id,
        )
        .join(
            latest_price,
            latest_price.c.store_product_id == StoreProduct.id,
        )
        .join(
            PriceHistory,
            and_(
                PriceHistory.store_product_id == StoreProduct.id,
                PriceHistory.captured_at
                == latest_price.c.latest_captured_at,
            ),
        )
        .filter(StoreProduct.product_id == product_id)
        .order_by(PriceHistory.price.asc())
        .all()
    )

    return {
        "product": product.name,
        "ean": product.ean,
        "offers": [
            {
                "store": row.store_name,
                "chain": row.chain_name,
                "price": row.price,
                "currency": row.currency,
            }
            for row in results
        ],
    }