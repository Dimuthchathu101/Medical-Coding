"""
Security utility functions (encryption, password hashing, etc.).
"""
from flask_login import current_user
from functools import wraps
from flask import flash, redirect, url_for

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash('You do not have permission to access this resource.')
                return redirect(url_for('patients.list_patients'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator 