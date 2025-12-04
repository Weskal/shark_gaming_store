from flask import Flask
from .config import Config
from .database import db
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # extensões
    db.init_app(app)
    JWTManager(app)

    # blueprints
    from .routes.auth import bp as auth_bp
    from .routes.products import bp as products_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)

    # criar tabelas 
    with app.app_context():
        db.create_all()

    return app