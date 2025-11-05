import os
from typing import Optional
from dotenv import load_dotenv

# Load .env if present for local development
load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "offers-backend")
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me_to_a_long_random_string")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

    SUPERADMIN_USERNAME: str = os.getenv("SUPERADMIN_USERNAME", "admin")
    SUPERADMIN_PASSWORD: str = os.getenv("SUPERADMIN_PASSWORD", "admin123")

    # Prefer full DATABASE_URL if provided
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "offers")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")

    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", os.path.abspath(os.path.join(os.getcwd(), "uploads")))
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()

# Ensure uploads directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
