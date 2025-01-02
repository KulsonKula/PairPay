from flask import Flask
from flask_cors import CORS
from app.config import config_by_name
from app.db import db
from app.routes.bill_api import bill_bp
from app.routes.user_api import user_bp
from app.routes.debt_api import debt_bp
from app.routes.friendship_api import friend_bp
from app.routes.expense_api import expense_bp
from app.routes.auth import auth_bp
from app.db.db_init import init_db
from flask_jwt_extended import JWTManager
from app.models import TokenBlocklist
from flask_mail import Mail


class AppFactory:
    def __init__(self, config_name="development"):
        self.config_name = config_name
        self.app = Flask(__name__)
        self.mail = Mail()

    def _load_config(self):
        self.app.config.from_object(
            config_by_name.get(self.config_name, config_by_name["development"])
        )

    def _initialize_cors(self):
        CORS(
            self.app,
            resources={
                r"/*": {
                    "origins": self.app.config["CORS_ORIGINS"],
                    "methods": self.app.config["CORS_METHODS"],
                    "allow_headers": self.app.config["CORS_ALLOW_HEADERS"],
                }
            },
        )

    def _register_blueprints(self):
        self.app.register_blueprint(auth_bp)
        self.app.register_blueprint(user_bp)
        self.app.register_blueprint(bill_bp, url_prefix="/api")
        self.app.register_blueprint(friend_bp, url_prefix="/api")
        self.app.register_blueprint(expense_bp, url_prefix="/api")
        self.app.register_blueprint(debt_bp)

    def _initialize_db(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            init_db()

    def _initialize_jwt(self):
        self.jwt = JWTManager(self.app)

        @self.jwt.token_in_blocklist_loader
        def check_if_token_in_blocklist(jwt_header, jwt_payload):
            jti = jwt_payload["jti"]
            return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    def _initialize_mail(self):
        self.mail.init_app(self.app)

    def create_app(self):
        self._load_config()
        self._initialize_cors()
        self._initialize_db()
        self._initialize_jwt()
        self._register_blueprints()
        self._initialize_mail()
        return self.app


def create_app(config_name="development"):
    factory = AppFactory(config_name)
    return factory.create_app()
