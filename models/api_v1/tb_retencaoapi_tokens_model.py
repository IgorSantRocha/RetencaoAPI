from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from datetime import datetime, timedelta
from db.base_class import Base


class RetencaoAPITokensModel(Base):
    # tabela no 212
    __tablename__ = 'TB_RetencaoAPI_Tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    apikey = Column("apikey", String(36))
    nome = Column("nome", String(10))
    list_permissions = Column("list_permissions", String(30))


class APITokensModel(Base):
    # tabela no 211
    __tablename__ = 'TB_API_Tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    criadoem = Column(DateTime, default=datetime.now())
    usr = Column("usr", String(50))
    token = Column("token", String(6))
    expiraem = Column(
        DateTime, default=lambda: datetime.now() + timedelta(minutes=10))
    usado = Column("usado", Boolean, default=False)
