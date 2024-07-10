from sqlalchemy import Column, Integer, String
from db.base_class import Base


class ListaProjetoModel(Base):
    __tablename__ = 'TB_PROJETO_FD'
    id = Column("id", Integer)
    codigo = Column("CODIGO", String(50))
    projeto = Column("PROJETO", String(250))
    fase = Column("FASE", String(10))
    cliente = Column("CLIENTE", String(100))
