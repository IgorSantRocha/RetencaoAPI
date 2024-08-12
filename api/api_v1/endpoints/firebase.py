import logging
import uuid
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException
from core.config import firebase_bucket
import os

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Extrai a extensão do arquivo
        file_extension = os.path.splitext(file.filename)[1]
        # Extrai o nome do arquivo sem a extensão
        file_name = os.path.splitext(file.filename)[0]
        # Gera um nome de arquivo único mantendo o nome original e adicionando UUID
        unique_filename = f"{file_name}_{uuid.uuid4()}{file_extension}"
        blob = firebase_bucket.blob(unique_filename)
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()

        return {"url": blob.public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/{imgname}")
async def upload_image_imgname(imgname: str, file: UploadFile = File(...)):
    try:
        # Extrai a extensão do arquivo
        file_extension = os.path.splitext(file.filename)[1]
        # Extrai o nome do arquivo sem a extensão
        file_name = imgname
        # Gera um nome de arquivo único mantendo o nome original e adicionando UUID
        unique_filename = f"{file_name}_{uuid.uuid4()}{file_extension}"
        blob = firebase_bucket.blob(unique_filename)
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()

        return {"url": blob.public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
