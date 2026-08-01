from pydantic_settings import BaseSettings, SettingsConfigDict


_base_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
        )


class DBSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str
    POSTGRES_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = _base_config

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def REDIS_URL(self, db):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}"

db_settings = DBSettings()




