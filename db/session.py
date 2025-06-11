from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from core.config import settings

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_size=5,        # Até 10 conexões persistentes no pool
    max_overflow=60,     # Até 20 conexões extras temporárias
    pool_timeout=60,     # Espera até 30s por uma conexão livre antes de erro
    pool_recycle=900,   # Fecha conexões inativas após 30 min (1800s)
    pool_pre_ping=True   # Testa conexões antes de usar (evita conexões mortas)
)


SQLAlchemyInstrumentor().instrument(
    engine=engine
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


engine_211 = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI_211), pool_pre_ping=True)
SQLAlchemyInstrumentor().instrument(
    engine=engine_211
)
SessionLocal_211 = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_211)
