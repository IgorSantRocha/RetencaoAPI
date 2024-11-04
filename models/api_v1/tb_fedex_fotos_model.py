from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from db.base_class import Base


class TbFedexFotosModel(Base):
    __tablename__ = 'TB_FEDEX_FOTOS'
    # "implicit_returning=false" não é recomendado. Usar somente se a tabela possuir Triggers(Gatilhos)
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_abertura = Column(DateTime, default=datetime.now())
    os = Column("os", String(250))
    longitude = Column("longitude", String(250))
    latitude = Column("latitude", String(250))
    imageurl = Column("imageurl", String(250))
    uid = Column("uid", Integer)
