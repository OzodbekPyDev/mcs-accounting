from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    PORT: int
    ECHO: bool = False
    ACCESS_PAYMENTS_TOKEN: str
    DOCS_MCS_URL: str
    CABINET_MCS_URL: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    api_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
