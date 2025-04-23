from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    PG_NAME: str
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str

settings = AppSettings(_env_file='.env', _env_file_encoding='utf-8') # type: ignore

