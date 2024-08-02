from fastapi import FastAPI, Depends, HTTPException, Security, status
from core.config import settings
from sqlalchemy.orm import Session
from crud.crud_tb_retencaoapi_tokens import tb_retencaoapi_tokens
from api import deps
from schemas.apikey_schema import APIKeyPerson


async def busca_meio_captura(apikey: APIKeyPerson = Security(settings.api_key_header), db: Session = Depends(deps.get_db)) -> str:
    '''
    Consulto a apikey na tabela e caso seja válida, retorno o nome do meio de captura
    '''
    meio_abertura = tb_retencaoapi_tokens.get_first_by_filter(
        db=db, filterby='apikey', filter=apikey)
    if not meio_abertura:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Não foi possível validar API KEY')

    result_apikey = APIKeyPerson(
        apikey=apikey, meio_abertura=meio_abertura.nome)

    return result_apikey
