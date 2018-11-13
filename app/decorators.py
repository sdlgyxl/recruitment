from functools import wraps
from flask import abort
from flask_login import current_user
from .models.user import User

def role_required(rolename):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.hasrole(rolename):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
