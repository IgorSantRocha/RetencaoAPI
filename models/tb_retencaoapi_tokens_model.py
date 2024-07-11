from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from db.base_class import Base


class RetencaoAPITokensModel(Base):
    __tablename__ = 'TB_RetencaoAPI_Tokens'
    id = Column("id", Integer)
    apikey = Column("apikey", String(36))
    nome = Column("nome", String(10))
    list_permissions = Column("list_permissions", String(30))
