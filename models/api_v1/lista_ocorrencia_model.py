from sqlalchemy import Column, Integer, String
from db.base_class import Base


class ListaOcorrenciaModel(Base):
    __tablename__ = 'Motivos_fedex'
    motivo: str = Column(String(250))
    id = Column(Integer, primary_key=True, autoincrement=True)
    projeto: str = Column(String(250))
