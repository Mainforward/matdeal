from decimal import Decimal
from uuid import UUID

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

class ProductCreate(BaseModel):
    ean: str | None = None
    name: str
    brand: str | None = None
    size_value: float | None = None
    size_unit: str | None = None
    category: str | None = None
    image_url: str | None = None