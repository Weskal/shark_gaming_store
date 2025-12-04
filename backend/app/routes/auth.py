from flask import Blueprint, request
# Age como um ponteiro apontando para o app principal, para manter o contexto...
from flask import current_app as app
from ..services.auth_service import register_user, authenticate_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post('/register')
def register():
    
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return {"message": "username e password são obrigatórios"}, 400
    
    try:
        user = register_user(username=username, password=password)
    except ValueError as e:
        return {"message": str(e)}, 400
    
    return {"id": user.id, "username": user.username}, 201

@bp.post('/login')
def login():
    
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return {"message": "username e password são obrigatórios"}, 400
    
    user = authenticate_user(username, password)
    if not user:
        return {"message": "credenciais inválidas"}
    
    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}, 200

@bp.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity
    return {"user_id": user_id}, 200
    