
import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Store(Base):
    __tablename__ = "stores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key = True,
        default=uuid.uuid4
    )

    chain_name: Mapped[str] = mapped_column(String(100))

    store_name: Mapped[str] = mapped_column(String(200))

    city: Mapped[str] = mapped_column(String(100))