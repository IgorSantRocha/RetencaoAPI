from crud.base import CRUDBase
from models.api_v1.usr_model import UsrAgModel, UsrRetModel
from schemas.api_v1.usr_schema import UsrAgSC, UsrRetSC


class CRUDItem_211(CRUDBase[UsrAgModel, UsrAgSC, UsrAgSC]):
    pass


user_211 = CRUDItem_211(UsrAgModel)


class CRUDItem_212(CRUDBase[UsrRetModel, UsrRetSC, UsrRetSC]):
    pass


user_212 = CRUDItem_212(UsrRetModel)
