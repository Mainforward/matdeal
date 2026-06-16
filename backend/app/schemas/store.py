
from pydantic import BaseModel
from uuid import UUID

class StoreBase(BaseModel):
    chain_name: str
    store_name: str
    city: str


class StoreCreate(StoreBase):
    pass


class StoreRead(StoreBase):
    id: UUID

    class Config:
        from_attributes = True
