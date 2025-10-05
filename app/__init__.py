from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    from app.routes import root_bp
    app.register_blueprint(root_bp)

    from app.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app
