import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///medical_coding.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    # Add more security and compliance settings as needed 

class DevelopmentConfig(Config):
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    DEBUG = True

# Select config based on environment
config = Config
if os.environ.get('FLASK_ENV') == 'development':
    config = DevelopmentConfig 