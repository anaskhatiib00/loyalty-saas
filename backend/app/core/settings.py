from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Apple Wallet
    APPLE_TEAM_IDENTIFIER: str | None = None
    APPLE_PASS_TYPE_IDENTIFIER: str | None = None
    APPLE_WWDR_CERT_PATH: str | None = None
    APPLE_SIGNER_CERT_PATH: str | None = None
    APPLE_SIGNER_KEY_PATH: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()