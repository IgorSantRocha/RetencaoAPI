from crud.base import CRUDBase
from models.api_v1.tb_projeto_fedex_historico_model import TbProjetoFDHistModel
from schemas.api_v1.tb_projeto_fedex_historico_schema import TbProjetoFedexHistoricoCreateSC, TbProjetoFedexHistoricoUpdate


class CRUDItem(CRUDBase[TbProjetoFDHistModel, TbProjetoFedexHistoricoCreateSC, TbProjetoFedexHistoricoUpdate]):
    pass


tb_projeto_fd_hist = CRUDItem(TbProjetoFDHistModel)
