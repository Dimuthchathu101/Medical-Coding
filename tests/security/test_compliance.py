import pytest
from unittest.mock import patch, MagicMock
from app.utils.compliance import log_audit

@pytest.fixture
def mock_db():
    with patch('app.utils.compliance.db') as db:
        yield db

@pytest.fixture
def mock_auditlog():
    with patch('app.utils.compliance.AuditLog') as AuditLog:
        yield AuditLog

def make_user(authenticated=True, user_id=1):
    user = MagicMock()
    user.is_authenticated = authenticated
    user.id = user_id
    return user

def test_log_audit_authenticated_user(mock_db, mock_auditlog):
    user = make_user(True, 42)
    with patch('app.utils.compliance.current_user', user):
        log_audit('test_action', 'TestType', 123, 'details')
        mock_auditlog.assert_called_once_with(
            user_id=42,
            action='test_action',
            target_type='TestType',
            target_id=123,
            details='details'
        )
        mock_db.session.add.assert_called()
        mock_db.session.commit.assert_called()

def test_log_audit_unauthenticated_user(mock_db, mock_auditlog):
    user = make_user(False, None)
    with patch('app.utils.compliance.current_user', user):
        log_audit('test_action', 'TestType', 123, 'details')
        mock_auditlog.assert_called_once_with(
            user_id=None,
            action='test_action',
            target_type='TestType',
            target_id=123,
            details='details'
        )
        mock_db.session.add.assert_called()
        mock_db.session.commit.assert_called() 