from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from db.base_class import Base


class UsrAgModel(Base):
    __tablename__ = 'usr'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usr = Column("usr", String(50))
    nome = Column("nome", String(50))
    niveldescricao = Column("NivelDescricao", String(50))
    pwd = Column("pwd", String(50))
    email = Column("email", String(250))


class UsrRetModel(Base):
    __tablename__ = 'usuario_fedex'
    usr = Column("usr", String(250))
    nome = Column("nome", String(250))
    pwd = Column("pwd", String(50))
    id = Column("id", Integer)
    nivel = Column("nivel", String(15))
