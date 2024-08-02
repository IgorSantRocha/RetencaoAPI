from crud.base import CRUDBase
from models.tb_projeto_fedex_model import TbProjetoFDModel
from schemas.tb_projeto_fedex_schema import TbProjetoFedexCreateSC


class CRUDItem(CRUDBase[TbProjetoFDModel, TbProjetoFedexCreateSC, TbProjetoFedexCreateSC]):
    pass


tb_projeto_fd = CRUDItem(TbProjetoFDModel)
