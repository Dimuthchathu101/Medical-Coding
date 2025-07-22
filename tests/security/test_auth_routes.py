import pytest
from flask import Flask, get_flashed_messages, session
from app.routes.auth import auth_bp
from app.models import User
from unittest.mock import patch, MagicMock
from flask_login import LoginManager
import flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Dummy user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return None

    # Dummy endpoint for patients.list_patients that renders flashed messages
    @app.route('/patients/')
    def list_patients():
        messages = get_flashed_messages()
        return ' '.join(messages) or 'Patients list page'
    app.add_url_rule('/patients/', endpoint='patients.list_patients', view_func=list_patients)

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def render_template_side_effect(template_name, *args, **kwargs):
    if template_name in ('login.html', 'register.html'):
        return 'dummy template'
    return flask.render_template(template_name, *args, **kwargs)

def get_flashed(client):
    with client.session_transaction() as sess:
        flashes = sess.get('_flashes', [])
        return [msg for cat, msg in flashes]

def test_register_unique_user(client):
    with patch('app.routes.auth.User') as MockUser, \
         patch('app.routes.auth.db') as mock_db, \
         patch('app.routes.auth.render_template', side_effect=render_template_side_effect):
        MockUser.query.filter.return_value.first.return_value = None
        user_instance = MagicMock()
        MockUser.return_value = user_instance
        response = client.post('/auth/register', data={
            'username': 'uniqueuser',
            'email': 'unique@example.com',
            'password': 'securepassword',
            'role': 'coder'
        }, follow_redirects=False)
        flashes = get_flashed(client)
        assert 'Registration successful. Please log in.' in flashes
        user_instance.set_password.assert_called_once_with('securepassword')
        mock_db.session.add.assert_called()
        mock_db.session.commit.assert_called()

def test_register_duplicate_user(client):
    with patch('app.routes.auth.User') as MockUser, \
         patch('app.routes.auth.render_template', side_effect=render_template_side_effect):
        MockUser.query.filter.return_value.first.return_value = True
        response = client.post('/auth/register', data={
            'username': 'existing',
            'email': 'existing@example.com',
            'password': 'securepassword',
            'role': 'coder'
        }, follow_redirects=False)
        flashes = get_flashed(client)
        assert 'Username or email already exists' in flashes

def test_login_correct_credentials(client):
    user = MagicMock()
    user.check_password.return_value = True
    with patch('app.routes.auth.User') as MockUser, \
         patch('app.routes.auth.login_user') as mock_login_user, \
         patch('app.routes.auth.render_template', side_effect=render_template_side_effect):
        MockUser.query.filter_by.return_value.first.return_value = user
        response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=False)
        flashes = get_flashed(client)
        assert 'Logged in successfully.' in flashes
        mock_login_user.assert_called_once_with(user)

def test_login_incorrect_credentials(client):
    user = MagicMock()
    user.check_password.return_value = False
    with patch('app.routes.auth.User') as MockUser, \
         patch('app.routes.auth.render_template', side_effect=render_template_side_effect):
        MockUser.query.filter_by.return_value.first.return_value = user
        response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'wrongpassword'
        }, follow_redirects=False)
        flashes = get_flashed(client)
        assert 'Invalid username or password' in flashes

def test_login_nonexistent_user(client):
    with patch('app.routes.auth.User') as MockUser, \
         patch('app.routes.auth.render_template', side_effect=render_template_side_effect):
        MockUser.query.filter_by.return_value.first.return_value = None
        response = client.post('/auth/login', data={
            'username': 'nouser',
            'password': 'nopass'
        }, follow_redirects=False)
        flashes = get_flashed(client)
        assert 'Invalid username or password' in flashes

def test_logout(client):
    # Patch current_user to be authenticated for logout
    mock_user = MagicMock()
    mock_user.is_authenticated = True
    with patch('app.routes.auth.logout_user') as mock_logout_user, \
         patch('flask_login.utils._get_user', return_value=mock_user), \
         patch('app.routes.auth.render_template', side_effect=render_template_side_effect):
        # Simulate logged-in user by setting session
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        response = client.get('/auth/logout', follow_redirects=False)
        flashes = get_flashed(client)
        assert 'You have been logged out.' in flashes
        mock_logout_user.assert_called_once() 