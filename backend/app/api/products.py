from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.product import Product
from app.models.store_product import StoreProduct
from app.models.store import Store
from app.models.price_history import PriceHistory

from uuid import UUID

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/{product_id}/offers")
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

    store_products = (
        db.query(StoreProduct)
        .filter(StoreProduct.product_id == product_id)
        .all()
    )

    offers = []

    for store_product in store_products:
        latest_price = (
            db.query(PriceHistory)
            .filter(
                PriceHistory.store_product_id == store_product.id
            )
            .order_by(PriceHistory.captured_at.desc())
            .first()
        )

        if latest_price:
            store = (
                db.query(Store)
                .filter(Store.id == store_product.store_id)
                .first()
            )

            offers.append(
                {
                    "store": store.store_name,
                    "chain": store.chain_name,
                    "price": latest_price.price,
                    "currency": latest_price.currency,

                }
            )
    
    offers.sort(key=lambda offer: offer["price"])

    return {
        "product": product.name,
        "ean": product.ean,
        "offers": offers,
    }