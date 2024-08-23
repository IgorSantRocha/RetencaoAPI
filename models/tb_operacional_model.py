from sqlalchemy import Column, Integer, String, Boolean
from db.base_class import Base


class TbOperacionalModel(Base):
    __tablename__ = 'TB_FEDEX_OPERACIONAL'
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo: str = Column(String(50), nullable=True)
    conclusao_operador: str = Column(String(50), nullable=False)
    protocolo: bool = Column(Boolean, nullable=False)
