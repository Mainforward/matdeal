

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.store import Store
from app.schemas.store import StoreRead

app = FastAPI(title="MatDeal API")

@app.get("/health")
async def healt():
    return {"staus": "ok"}

@app.get("/stores")
def get_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()
