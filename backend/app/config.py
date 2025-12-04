import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:admin@localhost:5432/techsolutions")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret Key do JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # Configurações do Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    PRODUCT_QUEUE = os.getenv("PRODUCT_QUEUE", "product_queue")