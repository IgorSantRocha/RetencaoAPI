from crud.base import CRUDBase
from models.api_v1.tb_fedex_fotos_model import TbFedexFotosModel
from schemas.api_v1.tb_fedex_fotos_schema import TbFedexFotosCreateSC, TbFedexFotosUpdate


class CRUDItem(CRUDBase[TbFedexFotosModel, TbFedexFotosCreateSC, TbFedexFotosUpdate]):
    pass


tb_fedex_fotos = CRUDItem(TbFedexFotosModel)
