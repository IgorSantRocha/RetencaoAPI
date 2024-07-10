from sqlalchemy import Column, Integer, String, Text, DateTime
from db.base_class import Base


class Car(Base):
    __tablename__ = 'TB_PROJETO_FEDEX'
    # "implicit_returning=false" não é recomendado. Usar somente se a tabela possuir Triggers(Gatilhos)
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    dt_abertura = Column(DateTime)
    atendente_abertura: str = Column(String(250), nullable=True)
    retorno_tecnico: str = Column(String(250), nullable=True)
    nome_tecnico: str = Column(String(250), nullable=True)
    telefone_tecnico: str = Column(String(250), nullable=True)
    os: str = Column(String(250))
    problema_apresentado: str = Column(Text, nullable=True)
    ocorrencia: str = Column(String(250), nullable=True)
    acao_D29: str = Column(String(250), nullable=True)
    projeto: str = Column(String(250), nullable=True)
    tipo_atendimento: str = Column(String(250), nullable=True)
    status: str = Column(String(250), nullable=True)
    subprojeto: str = Column(String(250), nullable=True)
    cliente: str = Column(String(250), nullable=True)
    versao: str = Column(String(250), nullable=True)
    chave: str = Column(String(250), nullable=True)
    dt_fechamento = Column(DateTime, nullable=True)
    fase: str = Column(String(250), nullable=True)
    conclusao_operador: str = Column(String(250), nullable=True)
    definicao: str = Column(String(250), nullable=True)
    status_relatorio: str = Column(String(250), nullable=True)
    etapa: str = Column(String(250), nullable=True)
    tipo: str = Column(String(250), nullable=True)
    acao_d1: str = Column(String(250), nullable=True)
    call_id: str = Column(String(250), nullable=True)
