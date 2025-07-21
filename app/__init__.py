from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_migrate import Migrate
from flask_principal import Principal
import os

# Initialize extensions
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
principals = Principal()

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get('APP_SETTINGS', 'config.Config'))

    # Security headers
    Talisman(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    principals.init_app(app)

    # Register blueprints (to be implemented)
    # from .routes.auth import auth_bp
    # app.register_blueprint(auth_bp)
    # from .routes.patients import patients_bp
    # app.register_blueprint(patients_bp)

    return app 