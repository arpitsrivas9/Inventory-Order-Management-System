from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: Optional[str] = None
    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_db: str = "inventory"
    postgres_user: str = "inventory_user"
    postgres_password: str = "inventory_pass"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def db_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
