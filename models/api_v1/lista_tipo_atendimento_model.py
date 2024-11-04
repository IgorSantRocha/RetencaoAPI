from sqlalchemy import Column, Integer, String
from db.base_class import Base


class ListaTipoAtendimentoModel(Base):
    __tablename__ = 'TB_TIPO_ATENDIMENTO'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Tipo_Atendimento: str = Column(String(250))
