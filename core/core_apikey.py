from fastapi import FastAPI, Depends, HTTPException, Security, status
from core.config import settings
from sqlalchemy.orm import Session
from crud.crud_tb_retencaoapi_tokens import tb_retencaoapi_tokens
from api import deps


async def get_api_key(api_key_header: str = Security(settings.api_key_header)):
    if api_key_header == settings.API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )


async def busca_meio_captura(apikey: str, db: Session = Depends(deps.get_db)) -> str:
    meio_abertura = tb_retencaoapi_tokens.get_first_by_filter(
        db=db, filterby='apikey', filter=apikey)
    if not meio_abertura:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='A chave informada não é válida!')

    return meio_abertura.nome
