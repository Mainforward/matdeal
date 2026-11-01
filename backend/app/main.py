

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.api.products import router as products_router
from app.db.dependencies import get_db
from app.models.store import Store
from app.schemas.store import StoreRead, StoreCreate

from app.api.store_products import router as store_products_router
from app.api.prices import router as prices_router


app = FastAPI(title="MatDeal API")

app.include_router(products_router)
app.include_router(store_products_router)
app.include_router(prices_router)

@app.get("/health")
async def healt():
    return {"staus": "ok"}

@app.get("/stores")
def get_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()

@app.post(
    "/stores",
    response_model=StoreRead,
    status_code=201,
)
def create_store(
    store_data: StoreCreate,
    db: Session = Depends(get_db),
):
    store = Store(
        chain_name=store_data.chain_name,
        store_name=store_data.store_name,
        city=store_data.city,
    )
    db.add(store)
    db.commit()
    db.refresh(store)

    return store
