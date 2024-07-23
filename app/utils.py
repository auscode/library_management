from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_identity()
            if claims['role'] != required_role:
                return jsonify({'message': 'Access denied'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
