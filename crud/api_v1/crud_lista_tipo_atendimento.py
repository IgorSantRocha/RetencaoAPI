from crud.base import CRUDBase
from models.api_v1.lista_tipo_atendimento_model import ListaTipoAtendimentoModel
from schemas.api_v1.tipo_atendimento_schema import TipoAtendimentoCreateSC, TipoAtendimentoUpdateSC


class CRUDItem(CRUDBase[ListaTipoAtendimentoModel, TipoAtendimentoCreateSC, TipoAtendimentoUpdateSC]):
    pass


lista_tipo_atendimento = CRUDItem(ListaTipoAtendimentoModel)
