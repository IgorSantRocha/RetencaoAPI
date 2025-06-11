from crud.base import CRUDBase
from models.base_cep_model import BaseCepModel
from schemas.base_cep_schema import BaseCepBaseSC, BaseCepCreateSC, BaseCepUpdateSC, BaseCepInDbBaseSC, BaseCepSC


class CRUDItem(CRUDBase[BaseCepModel, BaseCepCreateSC, BaseCepUpdateSC]):
    pass


crud_base_cep = CRUDItem(BaseCepModel)
