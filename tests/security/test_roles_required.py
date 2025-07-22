import pytest
from flask import Flask, redirect, url_for, get_flashed_messages
from flask_login import AnonymousUserMixin
from app.utils.security import roles_required
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'

    @app.route('/protected')
    @roles_required('admin', 'coder')
    def protected():
        return 'Access granted'

    # Dummy endpoint for redirect
    @app.route('/patients/')
    def list_patients():
        messages = get_flashed_messages()
        return ' '.join(messages) or 'Patients list page'

    # Register endpoint name for url_for
    app.add_url_rule('/patients/', endpoint='patients.list_patients', view_func=list_patients)

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def make_user(authenticated=True, role='admin'):
    user = MagicMock()
    user.is_authenticated = authenticated
    user.role = role
    return user

def test_access_granted_for_admin(client):
    with patch('app.utils.security.current_user', make_user(True, 'admin')):
        response = client.get('/protected', follow_redirects=True)
        assert b'Access granted' in response.data

def test_access_granted_for_coder(client):
    with patch('app.utils.security.current_user', make_user(True, 'coder')):
        response = client.get('/protected', follow_redirects=True)
        assert b'Access granted' in response.data

def test_access_denied_for_wrong_role(client):
    with patch('app.utils.security.current_user', make_user(True, 'viewer')):
        response = client.get('/protected', follow_redirects=True)
        assert b'You do not have permission' in response.data
        assert b'Access granted' not in response.data

def test_access_denied_for_unauthenticated(client):
    with patch('app.utils.security.current_user', new_callable=AnonymousUserMixin):
        response = client.get('/protected', follow_redirects=True)
        assert b'You do not have permission' in response.data
        assert b'Access granted' not in response.data 