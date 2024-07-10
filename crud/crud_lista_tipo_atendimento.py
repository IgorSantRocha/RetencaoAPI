from crud.base import CRUDBase
from models.lista_tipo_atendimento_model import ListaTipoAtendimentoModel
from schemas.tipo_atendimento_schema import TipoAtendimentoCreateSC, TipoAtendimentoUpdateSC


class CRUDItem(CRUDBase[ListaTipoAtendimentoModel, TipoAtendimentoCreateSC, TipoAtendimentoUpdateSC]):
    pass


lista_tipo_atendimento = CRUDItem(ListaTipoAtendimentoModel)
