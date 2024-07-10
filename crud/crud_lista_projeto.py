from crud.base import CRUDBase
from models.lista_projeto_model import ListaProjetoModel
from schemas.lista_projeto_schema import ListaProjetoCreateSC, ListaProjetoUpdateSC


class CRUDItem(CRUDBase[ListaProjetoModel, ListaProjetoCreateSC, ListaProjetoUpdateSC]):
    pass


lista_projetos = CRUDItem(ListaProjetoModel)
