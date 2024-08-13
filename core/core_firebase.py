from datetime import datetime
from fastapi import File, Depends, UploadFile, HTTPException
from core.config import settings
from sqlalchemy.orm import Session
from crud.crud_tb_fedex_fotos import tb_fedex_fotos
from schemas.tb_fedex_fotos_schema import TbFedexFotosCreateSC, TbFedexFotosUploadSC

import os
from core.config import firebase_bucket
import uuid


async def uplodad_foto_fb(
        info_upload: TbFedexFotosUploadSC,
        db: Session,
        file: UploadFile = File(...)
) -> str:
    '''
    Salvo a geo e a foto na tabela de controle
    '''
    try:
        # Extrai a extensão do arquivo
        file_extension = os.path.splitext(file.filename)[1]
        # Extrai o nome do arquivo sem a extensão
        file_name = info_upload.os
        # Gera um nome de arquivo único mantendo o nome original e adicionando UUID
        unique_filename = f"{file_name}_{uuid.uuid4()}{file_extension}"
        blob = firebase_bucket.blob(unique_filename)
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()

        data_hora_atual = datetime.now()
        data_hora_formato_sql_server: str = data_hora_atual.strftime(
            "%Y-%m-%d %H:%M:%S.%f")[:-3]

        obj_foto_e_geo = TbFedexFotosCreateSC(
            os=info_upload.os,
            imageurl=blob.public_url,
            latitude=info_upload.latitude,
            longitude=info_upload.longitude,
            uid=info_upload.uid,
            data_abertura=data_hora_formato_sql_server
        )

        tb_fedex_fotos.create(db=db, obj_in=obj_foto_e_geo)

        return {"url": blob.public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
