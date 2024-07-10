from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from db.base_class import Base


class TbProjetoFDHistModel(Base):
    __tablename__ = 'TB_PROJETO_FEDEX_HISTORICO'
    # "implicit_returning=false" não é recomendado. Usar somente se a tabela possuir Triggers(Gatilhos)
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    dt_criado = Column(DateTime, default=datetime.now())
    os: str = Column(String(250))
    nr_atendimento: str = Column(String(250), nullable=True)
    problema_apresentado: str = Column(Text, nullable=True)
    tecnico: str = Column(String(250), nullable=True)
    callid: str = Column(String(250), nullable=True)
