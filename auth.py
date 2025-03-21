from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Bearer secret-token-123':
            return f(*args, **kwargs)
        return jsonify({"message": "Unauthorized"}), 401
    return decorated