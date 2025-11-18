from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./fitTogether.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "secret")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expiry: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

settings = Settings()