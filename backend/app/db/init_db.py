
from app.db.base import Base
from app.db.database import engine

from app.models import Product, Store, StoreProduct

def init_db():
    Base.metadata.create_all(bind=engine)
    print("DB initialized")

if __name__ == "__main__":
    init_db()