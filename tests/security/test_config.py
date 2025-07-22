import os
import pytest
from config import Config


def test_config_secure_cookies():
    assert Config.SESSION_COOKIE_SECURE is True
    assert Config.REMEMBER_COOKIE_SECURE is True

@pytest.mark.skipif(os.environ.get('FLASK_ENV') == 'development', reason='Default secret key allowed in development')
def test_config_secret_key_not_default():
    # Should not use the default in production
    assert Config.SECRET_KEY != 'change-this-in-production' 