from crud.base import CRUDBase
from models.api_v1.lista_ocorrencia_model import ListaOcorrenciaModel
from schemas.api_v1.ocorrencia_schema import ListaOcorrenciaCreateSC, ListaOcorrenciaUpdateSC


class CRUDItem(CRUDBase[ListaOcorrenciaModel, ListaOcorrenciaCreateSC, ListaOcorrenciaUpdateSC]):
    pass


lista_ocorrencia = CRUDItem(ListaOcorrenciaModel)
