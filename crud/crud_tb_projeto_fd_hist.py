from crud.base import CRUDBase
from models.tb_projeto_fedex_historico_model import TbProjetoFDHistModel
from schemas.tb_projeto_fedex_historico_schema import TbProjetoFedexHistoricoCreateSC, TbProjetoFedexHistoricoUpdate


class CRUDItem(CRUDBase[TbProjetoFDHistModel, TbProjetoFedexHistoricoCreateSC, TbProjetoFedexHistoricoUpdate]):
    pass


car = CRUDItem(TbProjetoFDHistModel)
