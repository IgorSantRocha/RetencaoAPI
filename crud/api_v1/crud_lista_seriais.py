from crud.base import CRUDBase
from models.api_v1.lista_seriais_model import ListaSeriaisModel
from schemas.api_v1.lista_seriais_schema import ListaSeriaisCreateSC, ListaSeriaisUpdateSC


class CRUDItem(CRUDBase[ListaSeriaisModel, ListaSeriaisCreateSC, ListaSeriaisUpdateSC]):
    pass


lista_seriais = CRUDItem(ListaSeriaisModel)
