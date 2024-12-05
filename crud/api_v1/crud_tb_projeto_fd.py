from crud.base import CRUDBase
from models.api_v1.tb_projeto_fedex_model import TbProjetoFDModel
from schemas.api_v1.tb_projeto_fedex_schema import TbProjetoFedexCreateSC, TbProjetoFedexSC, TbProjetoFedexUpdateCallidSC
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta


class CRUDItem(CRUDBase[TbProjetoFDModel, TbProjetoFedexCreateSC, TbProjetoFedexCreateSC]):
    def get_recente(self, db: Session, uid: int, cliente: str) -> list[TbProjetoFedexSC]:

        hora_dif = datetime.now() - timedelta(days=5)
        consulta = db.query(self.model).filter(
            self.model.uid == uid,
            self.model.cliente == cliente,
            self.model.dt_abertura >= hora_dif
        ).order_by(desc(self.model.dt_fechamento)).all()

        return consulta


class CRUDItemCallid(CRUDBase[TbProjetoFDModel, TbProjetoFedexUpdateCallidSC, TbProjetoFedexUpdateCallidSC]):
    def get_recente(self, db: Session, uid: int, cliente: str) -> list[TbProjetoFedexSC]:

        hora_dif = datetime.now() - timedelta(days=5)
        consulta = db.query(self.model).filter(
            self.model.uid == uid,
            self.model.cliente == cliente,
            self.model.dt_abertura >= hora_dif
        ).all()

        return consulta


tb_projeto_fd = CRUDItem(TbProjetoFDModel)

tb_projeto_fd_callid = CRUDItemCallid(TbProjetoFDModel)
