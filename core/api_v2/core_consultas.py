from sqlalchemy.ext.asyncio import AsyncSession
from schemas.api_v1.tb_fedex_fotos_schema import TbFedexFotosBaseConsultaSC
from schemas.api_v1.tb_projeto_fedex_schema import TbProjetoFedexSC
from crud.api_v1.crud_tb_fedex_fotos import tb_fedex_fotos
from crud.api_v1.crud_tb_projeto_fd import tb_projeto_fd


class Consultas:
    async def busca_lista_os_por_uid(self, uid: int, db: AsyncSession, cliente: str) -> list[TbProjetoFedexSC]:
        consulta = tb_projeto_fd.get_recente(db=db, uid=uid, cliente=cliente)

        return consulta

    async def busca_fotos_e_geo_os(self, os: str, db: AsyncSession) -> list[TbFedexFotosBaseConsultaSC]:
        fotos_e_geo: TbFedexFotosBaseConsultaSC = tb_fedex_fotos.get_multi_filter(
            db=db, filterby='os', filter=os)

        return fotos_e_geo
