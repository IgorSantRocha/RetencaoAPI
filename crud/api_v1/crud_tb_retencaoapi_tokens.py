from crud.base import CRUDBase
from models.api_v1.tb_retencaoapi_tokens_model import RetencaoAPITokensModel,APITokensModel
from schemas.api_v1.tb_retencaoapi_tokens_schema import RetencaoAPITokensCreateSC, RetencaoAPITokensUpdateSC
from schemas.api_v1.tb_retencaoapi_tokens_schema import APITokensCreateSC, APITokensUpdateSC


class CRUDItem(CRUDBase[RetencaoAPITokensModel, RetencaoAPITokensCreateSC, RetencaoAPITokensUpdateSC]):
    pass


tb_retencaoapi_tokens = CRUDItem(RetencaoAPITokensModel)


class CRUDItem2(CRUDBase[APITokensModel, APITokensCreateSC, APITokensUpdateSC]):
    pass


tb_api_tokens = CRUDItem2(APITokensModel)
