from sqlalchemy.ext.asyncio import AsyncSession
from schemas.lista_projeto_schema import ListaProjetoSC
from crud.crud_lista_projeto import lista_projetos


class Consultas:

    async def busca_lista_projetos(self, cliente: str, db: AsyncSession) -> list[ListaProjetoSC]:
        projetos = lista_projetos.get_multi(db=db)
        return projetos
