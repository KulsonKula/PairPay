from flask_cors import CORS


def configure_cors(app):
    CORS(app, resources={r"/*": {"origins": "*",
         "methods": ["GET", "POST"], "allow_headers": ["Content-Type"]}})
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
