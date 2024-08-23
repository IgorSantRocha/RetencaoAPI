from crud.base import CRUDBase
from models.tb_projeto_fedex_model import TbProjetoFDModel
from schemas.tb_projeto_fedex_schema import TbProjetoFedexCreateSC, TbProjetoFedexSC, TbProjetoFedexUpdateCallidSC
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


class CRUDItem(CRUDBase[TbProjetoFDModel, TbProjetoFedexCreateSC, TbProjetoFedexCreateSC]):
    def get_recente(self, db: Session, uid: int) -> list[TbProjetoFedexSC]:

        hora_dif = datetime.now() - timedelta(days=5)
        consulta = db.query(self.model).filter(
            self.model.uid == uid,
            self.model.dt_abertura >= hora_dif
        ).all()

        return consulta


class CRUDItemCallid(CRUDBase[TbProjetoFDModel, TbProjetoFedexUpdateCallidSC, TbProjetoFedexUpdateCallidSC]):
    def get_recente(self, db: Session, uid: int) -> list[TbProjetoFedexSC]:

        hora_dif = datetime.now() - timedelta(days=5)
        consulta = db.query(self.model).filter(
            self.model.uid == uid,
            self.model.dt_abertura >= hora_dif
        ).all()

        return consulta


tb_projeto_fd = CRUDItem(TbProjetoFDModel)

tb_projeto_fd_callid = CRUDItemCallid(TbProjetoFDModel)
