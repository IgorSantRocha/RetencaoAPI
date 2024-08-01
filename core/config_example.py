'''
Renomeie o módulo para config.py
'''
import secrets
from typing import Any, Dict, List, Optional, Union
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import AnyHttpUrl, AnyUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    API_VERSION: str = '0.0.2'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    API_KEY = "Sua_chave_vai_aqui"
    API_KEY_NAME = "access_token"
    api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    LOGGING_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {"handlers": ["default"], "level": "INFO", "propagate": False},
        },
    }

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = 'Retenção API'
    SQL_HOST: str = '127.0.0.1'
    SQL_USER: str = 'user'
    SQL_PASSWORD: str = 'pwd'
    SQL_DATABASE: str = 'fastapi_db'
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f'mssql+pyodbc://{values.get("SQL_USER")}:{values.get("SQL_PASSWORD")}@{values.get("SQL_HOST")}/{values.get("SQL_DATABASE")}?driver=ODBC+Driver+17+for+SQL+Server'

    class Config:
        case_sensitive = True

    TEMPO_URL: str = 'http://localhost:4317'


settings = Settings()