import logging
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException
from core.config import firebase_bucket

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        blob = firebase_bucket.blob(file.filename)
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()

        return {"url": blob.public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
