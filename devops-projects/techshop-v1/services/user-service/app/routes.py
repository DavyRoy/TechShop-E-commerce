import bcrypt
from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.auth import create_access_token, create_refresh_token, jwt_required

auth_bp = Blueprint('auth', __name__)

def error_response(code, message, status):
    return jsonify({'error': {'code': code, 'message': message, 'status': status}}), status

@auth_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'user-service'}), 200

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email    = data.get('email')
    password = data.get('password')
    name     = data.get('name')

    if not email or not password or not name:
        return error_response('VALIDATION_ERROR', 'email, password and name required', 400)

    if User.query.filter_by(email=email).first():
        return error_response('EMAIL_EXISTS', 'Email already registered', 409)

    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt(rounds=12)
    ).decode('utf-8')

    user = User(email=email, name=name, password=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({'data': {'user_id': user.id, 'email': user.email, 'name': user.name}}), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email    = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return error_response('INVALID_CREDENTIALS', 'Invalid email or password', 401)

    access_token  = create_access_token(user.id, user.email)
    refresh_token = create_refresh_token(user.id)

    return jsonify({'data': {'access_token': access_token, 'refresh_token': refresh_token, 'expires_in': 900}}), 200

@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required
def me():
    user = User.query.get(request.user_id)
    if not user:
        return error_response('USER_NOT_FOUND', 'User not found', 404)
    return jsonify({'data': {'user_id': user.id, 'email': user.email, 'name': user.name}}), 200

@auth_bp.route('/auth/refresh', methods=['POST'])
def refresh():
    data  = request.get_json()
    token = data.get('refresh_token')
    if not token:
        return error_response('VALIDATION_ERROR', 'refresh_token required', 400)

    import jwt as pyjwt
    from app.auth import JWT_SECRET_KEY
    try:
        payload      = pyjwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        access_token = create_access_token(payload['user_id'], '')
        return jsonify({'data': {'access_token': access_token, 'expires_in': 900}}), 200
    except pyjwt.ExpiredSignatureError:
        return error_response('TOKEN_EXPIRED', 'Refresh token expired', 401)
    except pyjwt.InvalidTokenError:
        return error_response('INVALID_TOKEN', 'Invalid refresh token', 401)

@auth_bp.route('/users/<user_id>', methods=['GET'])
@jwt_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return error_response('USER_NOT_FOUND', 'User not found', 404)
    return jsonify({'data': {'user_id': user.id, 'email': user.email, 'name': user.name}}), 200