from sqlalchemy import Column, Integer, String, Text, DateTime
from db.base_class import Base


class BaseCepModel(Base):
    __tablename__ = 'TB_BASE_IBGE_logradouros'

    id = Column("id_logradouro", Integer, primary_key=True, autoincrement=True)
    tipo = Column("tipo", String(50))
    logradouro = Column("logradouro", String(100))
    logradouro_sem_numero = Column("logradouro_sem_numero", String(100))
    complemento = Column("complemento", String(100))
    bairro = Column("bairro", String(100))
    cidade = Column("cidade", String(100))
    uf = Column("UF", String(2))
    cep = Column("CEP", String(11))
    codigo_cidade_ibge = Column("codigo_cidade_ibge", Integer)
