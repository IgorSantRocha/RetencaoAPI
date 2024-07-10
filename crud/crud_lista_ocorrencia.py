from crud.base import CRUDBase
from models.lista_ocorrencia_model import ListaOcorrenciaModel
from schemas.ocorrencia_schema import ListaOcorrenciaCreateSC, ListaOcorrenciaUpdateSC


class CRUDItem(CRUDBase[ListaOcorrenciaModel, ListaOcorrenciaCreateSC, ListaOcorrenciaUpdateSC]):
    pass


lista_ocorrencia = CRUDItem(ListaOcorrenciaModel)
