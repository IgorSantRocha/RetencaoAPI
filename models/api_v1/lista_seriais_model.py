from sqlalchemy import Column, Integer, String, DateTime
from db.base_class import Base


class ListaSeriaisModel(Base):
    __tablename__ = 'TB_SERIAL_COLETADO_POR_PEDIDO'
    id = Column(Integer, primary_key=True, autoincrement=True)
    serial = Column("SERIAL", String(50))
    os = Column("OS", String(50))
    criadoem = Column("CRIADOEM", DateTime)
    uid = Column("UID", Integer)
