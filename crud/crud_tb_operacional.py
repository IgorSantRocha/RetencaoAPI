from crud.base import CRUDBase
from models.tb_operacional_model import TbOperacionalModel
from schemas.tb_fedex_operacional_schema import TbFedexOpBaseSC


class CRUDItem(CRUDBase[TbOperacionalModel, TbFedexOpBaseSC, TbFedexOpBaseSC]):
    pass


tb_fedex_operacional = CRUDItem(TbOperacionalModel)
