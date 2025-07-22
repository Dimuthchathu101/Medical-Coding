"""
Compliance utility functions (audit logging, HIPAA checks, etc.).
"""
from app.models import AuditLog, db
from flask_login import current_user

def log_audit(action, target_type, target_id, details=None):
    audit = AuditLog(
        user_id=current_user.id if current_user.is_authenticated else None,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details
    )
    db.session.add(audit)
    db.session.commit() 