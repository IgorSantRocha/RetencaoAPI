from sqlalchemy.ext.asyncio import AsyncSession
from crud.crud_tb_retencaoapi_tokens import tb_retencaoapi_tokens
from fastapi import HTTPException, status
import re


class Token:
    async def valida_token(self, apikey: str, db: AsyncSession) -> str:
        meio_abertura = tb_retencaoapi_tokens.get_first_by_filter(
            db=db, filterby='apikey', filter=apikey)
        if not meio_abertura:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='A chave informada não é válida!')

        return meio_abertura.nome
