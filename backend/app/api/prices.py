from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import PriceHistory, StoreProduct
from app.schemas.product import PriceCreate

router = APIRouter(
    prefix="/prices",
    tags=["prices"],
)

@router.post("", status_code=201)
def create_price(
    data: PriceCreate,
    db: Session = Depends(get_db),
):
    store_product = (
        db.query(StoreProduct)
        .filter(StoreProduct.id == data.store_product_id)
        .first()
    )

    if store_product is None:
        raise HTTPException(
            status_code=404,
            detail="Store product not found"
        )
    
    price = PriceHistory(
        store_product_id=data.store_product_id,
        price=data.price,
        currency=data.currency,
        **(
            {"captured_at": data.captured_at}
            if data.captured_at is not None
            else {}
        ),
    )

    db.add(price)
    db.commit()
    db.refresh(price)

    return {
        "id": str(price.id),
        "store_product_id": str(price.store_product_id),
        "price": str(price.price),
        "currency": price.currency,
        "captured_at": price.captured_at.isoformat(),
    }
    