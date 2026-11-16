
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import Receipt
from app.schemas.receipt import ReceiptResponse

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/receipts",
    tags=["receipts"],
)

UPLOAD_DIR = Path("app/uploads/receipts")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "application/pdf": ".pdf",
}

@router.post(
    "",
    response_model=ReceiptResponse,
    status_code=201
)

async def upload_receipt(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    extension = ALLOWED_TYPES.get(file.content_type)

    if extension is None:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG, and PDF files are allowed"
        )
        
    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10 MB")
    
    file_id = uuid.uuid4()
    safe_filename = f"{file_id}{extension}"

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_path = UPLOAD_DIR / safe_filename

    try:
        file_path.write_bytes(content)

        receipt = Receipt(
            file_path=str(file_path),
            original_filename=file.filename or safe_filename,
            status="uploaded",
        )

        db.add(receipt)
        db.commit()
        db.refresh(receipt)
    
    except Exception:
        db.rollback()
        logger.exception("Receipt upload failed")

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(status_code=500, detail="Failed to upload receipt")


    return ReceiptResponse(
        id=receipt.id,
        store_id=receipt.store_id,
        original_filename=receipt.original_filename,
        status=receipt.status,
        created_at=receipt.created_at,
    )