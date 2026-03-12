import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret')

def create_access_token(user_id: str, email: str) -> str:
    payload = {
        'user_id': user_id,
        'email':   email,
        'exp':     datetime.utcnow() + timedelta(minutes=15),
        'type':    'access'
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def create_refresh_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp':     datetime.utcnow() + timedelta(days=7),
        'type':    'refresh'
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': {'code': 'UNAUTHORIZED', 'status': 401}}), 401

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': {'code': 'TOKEN_EXPIRED', 'status': 401}}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': {'code': 'INVALID_TOKEN', 'status': 401}}), 401

        return f(*args, **kwargs)
    return decorated