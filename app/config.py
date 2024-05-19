from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    '''Переменные окружения'''
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self) -> str:
        '''Получение строки подключения к Postgres'''
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def REDIS_URL(self) -> str:
        '''Получение строки подключения к Redis'''
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()