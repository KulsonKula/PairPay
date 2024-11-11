import os
from dotenv import load_dotenv

load_dotenv(".env.dev")


class Config:

    DEBUG = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
    CORS_ORIGINS = ["http://localhost:3000"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    DATABASE_URI = os.getenv("DATABASE_URL")
    TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 3600


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
