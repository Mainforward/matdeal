from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


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
    id: UUID
    ean: str | None
    name: str
    brand: str | None