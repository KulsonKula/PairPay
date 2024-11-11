import os
from dotenv import load_dotenv

load_dotenv(".env.dev")


class Config:
    def __init__(self, env):
        self.env = env
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
        self.CORS_ORIGINS = ["http://localhost:3000"]
        self.CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]
        self.MAX_CONTENT_LENGTH = 50 * 1024 * 1024
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.TRACK_MODIFICATIONS = False
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        self.JWT_ACCESS_TOKEN_EXPIRES = 3600

        self.configure_for_env()

    def configure_for_env(self):
        if self.env == "development":
            self.DEBUG = True
        elif self.env == "production":
            self.DEBUG = False


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__(env="development")


class ProductionConfig(Config):
    def __init__(self):
        super().__init__(env="production")


config_by_name = {
    "development": DevelopmentConfig(),
    "production": ProductionConfig(),
}
