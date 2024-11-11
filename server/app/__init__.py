import os
from flask import Flask
from flask_cors import CORS
from app.config import config_by_name
from app.db.db_init import init_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_app():
    app = Flask(__name__)

    config_name = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_name[config_name])

    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS'],
                                 "methods": app.config['CORS_METHODS'],
                                 "allow_headers": app.config['CORS_ALLOW_HEADERS']}})

    init_db()

    return app


def get_db_engine(app):
    return create_engine(app.config['DATABASE_URI'], pool_size=10, max_overflow=20)


def get_db_session(app):
    engine = get_db_engine(app)
    Session = sessionmaker(bind=engine)
    return Session()
