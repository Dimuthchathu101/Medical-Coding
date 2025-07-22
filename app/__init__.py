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
    if not app.debug and not app.testing:
        Talisman(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    principals.init_app(app)

    # Register blueprints (to be implemented)
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from .routes.patients import patients_bp
    app.register_blueprint(patients_bp, url_prefix='/patients')

    # Automatically create a default admin user if not exists
    with app.app_context():
        from app.models import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    @app.route('/')
    def home():
        from flask_login import current_user
        from flask import redirect, url_for
        if current_user.is_authenticated:
            return redirect(url_for('patients.list_patients'))
        return redirect(url_for('auth.login'))

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import here to avoid circular import
        return User.query.get(int(user_id))

    return app