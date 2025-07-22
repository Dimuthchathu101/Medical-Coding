import pytest
from app.models import User

def test_set_password_hashes_password():
    user = User(username='test', email='test@example.com', role='coder')
    user.set_password('securepassword')
    assert user.password_hash != 'securepassword'
    assert user.password_hash.startswith('scrypt:') or user.password_hash.startswith('pbkdf2:sha256:')

def test_check_password_correct():
    user = User(username='test', email='test@example.com', role='coder')
    user.set_password('securepassword')
    assert user.check_password('securepassword')

def test_check_password_incorrect():
    user = User(username='test', email='test@example.com', role='coder')
    user.set_password('securepassword')
    assert not user.check_password('wrongpassword') 