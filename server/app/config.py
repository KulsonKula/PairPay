import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv(".env.dev")


class Config:
    def __init__(self, env):
        self.env = env
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
        self.CORS_ORIGINS = [
            "http://localhost:5173",
            "http://localhost:4173",
            "http://localhost:80",
        ]
        self.CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]
        self.MAX_CONTENT_LENGTH = 50 * 1024 * 1024
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        self.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
        self.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
        # self.JWT_VERIFY_SUB = False

        # Konfiguracja e-mail
        self.MAIL_SERVER = "smtp.gmail.com"
        self.MAIL_PORT = 587
        self.MAIL_USE_TLS = True
        self.MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
        self.MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
        self.MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

        self.COMPRESS_ALGORITHM = "gzip"
        self.COMPRESS_LEVEL = 6
        self.COMPRESS_MIN_SIZE = 500

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
