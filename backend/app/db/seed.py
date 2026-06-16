
from app.db.database import SessionLocal
from app.models.store import Store

def seed():
    db = SessionLocal()

    try:
        existing = db.query(Store).first()

        if existing:
            print("DB already seeded")
            return

        stores = [
            Store(chain_name="Lidl", store_name="Lidl Spånga", city="Stockholm"),
            Store(chain_name="Coop", store_name="Stora Coop Spånga", city="Stockholm"),
            Store(chain_name="Hemköp", store_name="Hemköp Rissne Torg 7", city="Stockholm"),
        ]

        db.add_all(stores)
        db.commit()

        print("Seed completed")

    finally:
        db.close()

if __name__ == "__main__":
    seed()