
from app.db.database import SessionLocal
from app.models.store import Store

from app.models.product import Product
from app.models.store_product import StoreProduct

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

        products = [
            Product(
                ean = "7314874087009",
                name = "Frasrost bröd",
                brand = "Skogaholm bageri",
                size_value = 450,
                size_unit = "G",
                category = "Dairy",
            ),
            Product(
                ean="7310865004703",
                name="Mellanmjölk 1L",
                brand="Arla",
                size_value=1,
                size_unit="L",
                category="Dairy",
            )
        ]

        db.add_all(products)
        db.flush()

        store_products = [
            StoreProduct(
                store_id=stores[0].id,
                product_id=products[0].id,
                external_id="TEST-ARLA-001",
                external_name="Arla Mellanmjölk 1L",
                external_url="https://example.com/product",
                available=True,
            ),
            StoreProduct(
                store_id=stores[0].id,
                product_id=products[1].id,
                external_id="TEST-FRASROST-002",
                external_name="Frasrost bröd 450G",
                external_url="https://example.com/product",
                available=True,
            ),

        ]
        db.add_all(store_products)
        db.flush()

        db.commit()

        print("Seed completed")

    finally:
        db.close()

if __name__ == "__main__":
    seed()