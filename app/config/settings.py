from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str 
    DB_NAME: str 
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PRODUCT_FETCH_API: str
    GCS_BUCKET_NAME: str
    GCD_CREDENTIALS_JSON_PATH: str
    MAX_FILE_SIZE_MB : int

    class Config:
        env_file = ".env"

settings = Settings()
