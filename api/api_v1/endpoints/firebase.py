import logging
from fastapi import APIRouter, Depends
from fastapi import File, UploadFile, HTTPException, Form
from core.core_apikey import busca_meio_captura
from schemas.apikey_schema import APIKeyPerson
from schemas.tb_fedex_fotos_schema import TbFedexFotosUploadSC
from core.core_firebase import uplodad_foto_fb
from sqlalchemy.orm import Session
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload/")
async def upload_image_imgname(
    os: str = Form(...),
    latitude: str = Form(...),
    longitude: str = Form(...),
    uid: int = Form(...),
    file: UploadFile = File(...),
    api_key: APIKeyPerson = Depends(busca_meio_captura),
    db: Session = Depends(deps.get_db),
):
    info_upload = TbFedexFotosUploadSC(
        os=os, longitude=longitude, latitude=latitude, uid=uid)
    return await uplodad_foto_fb(info_upload=info_upload, file=file, db=db)
