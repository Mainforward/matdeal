import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Numeric
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID


from app.db.base import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    store_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stores.id"),
        nullable=True
    )

    purchased_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=True
    )

    total: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )

    currency: Mapped[str | None] = mapped_column(
        String(3),
        default="SEK",
    )

    file_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        "original_file_name",
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="uploaded",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )