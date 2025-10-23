from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
import os

# Inicialização das extensões
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///biblioteca.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .auth import auth_bp
    from .livros import livros_bp
    from .api import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(livros_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
