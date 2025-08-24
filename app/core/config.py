from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    MONGODB_URI: str = Field(..., description="MongoDB connection string")
    MONGODB_DB: str = Field(..., description="MongoDB database name")

    JWT_SECRET: str = Field(..., description="JWT signing secret")
    JWT_ALGORITHM: str = Field("HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRES_MIN: int = Field(60, description="Access Token TTL in minutes")

    APP_NAME: str = Field("Employee Leave & Payroll API")
    APP_ENV: str = Field("dev")
    APP_VERSION: str = Field("1.0.0")

    class Config:
        env_file = ".env"

settings = Settings()
