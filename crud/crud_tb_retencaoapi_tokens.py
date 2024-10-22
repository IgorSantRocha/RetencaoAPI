from crud.base import CRUDBase
from models.tb_retencaoapi_tokens_model import RetencaoAPITokensModel
from schemas.tb_retencaoapi_tokens_schema import RetencaoAPITokensCreateSC, RetencaoAPITokensUpdateSC


class CRUDItem(CRUDBase[RetencaoAPITokensModel, RetencaoAPITokensCreateSC, RetencaoAPITokensUpdateSC]):
    pass


tb_retencaoapi_tokens = CRUDItem(RetencaoAPITokensModel)
