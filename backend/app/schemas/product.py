from decimal import Decimal
from uuid import UUID
from datetime import datetime
from pydantic import Field

from pydantic import BaseModel, ConfigDict


class OfferResponse(BaseModel):
    store: str
    chain: str
    price: Decimal
    currency: str


class ProductOffersResponse(BaseModel):
    product: str
    ean: str | None
    offers: list[OfferResponse]

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ean: str | None
    name: str
    brand: str | None

# Create Canoniclal Product
class ProductCreate(BaseModel):
    ean: str | None = None
    name: str
    brand: str | None = None
    size_value: float | None = None
    size_unit: str | None = None
    category: str | None = None
    image_url: str | None = None

# Create Product in stores
class StoreProductCreate(BaseModel):
    store_id: UUID
    product_id: UUID
    external_id: str
    external_name: str
    external_url: str | None = None
    available: bool = True

class StoreProductResponse(BaseModel):
    id: UUID
    store_id: UUID
    product_id: UUID
    external_id: str
    external_name: str
    external_url: str | None
    available: bool

class PriceCreate(BaseModel):
    store_product_id: UUID
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    currency: str = "SEK"
    captured_at: datetime | None = None