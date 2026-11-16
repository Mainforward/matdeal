
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class ReceiptResponse(BaseModel):
    id: UUID
    store_id: UUID | None
    original_filename: str
    status: str
    created_at: datetime
