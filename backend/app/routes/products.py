from flask import Blueprint, jsonify, request, current_app
from app.models.product import Product
from ..database import db
from flask_jwt_extended import jwt_required
from ..services.product_service import get_all_products
from ..config import Config
import redis, json


bp = Blueprint('products', __name__, url_prefix='/products')

@bp.get('/')
@jwt_required()
def list_products():
    products = get_all_products()
    return jsonify([
        {"id": p.id, "name": p.name, "brand": p.brand, "price": float(p.price)}
        for p in products
    ])

def _get_redis():
    cfg = current_app.config
    return redis.Redis(host=cfg.get('REDIS_HOST', Config.REDIS_HOST),
    port=cfg.get('REDIS_PORT', Config.REDIS_PORT),
    db=cfg.get('REDIS_DB', Config.REDIS_DB),
    decode_responses=True)

@bp.post('/')
@jwt_required()
def create_product():
    data = request.get_json() or {}
    if not data.get('name') or not data.get('price'):
        return {"message": "nome e preço são obrigatórios"}
    
    message = {"op": "create", "data": {"name": data['name'], "brand": data.get('brand'), "price": str(data['price'])}}
    
    r = _get_redis()
    r.lpush(current_app.config.get('PRODUCT_QUEUE', 'product_queue'), json.dumps(message))
    
    return {"message": "enqueued"}, 202

@bp.put('/<int:product_id>')
@jwt_required()
def update_product(product_id):
    
    # Permitido leitura acessando diretamente a API
    p = db.session.get(Product, product_id)
    if not p:
        return {"error": "Produto não encontrado"}, 404
    data = request.get_json() or {}
    message = {"op": "update", "data": {"id": product_id, **data}}
    r = _get_redis()
    r.lpush(current_app.config.get('PRODUCT_QUEUE', 'product_queue'), json.dumps(message))
    return {"message": "enqueued"}, 202

@bp.delete('/<int:product_id>')
@jwt_required()
def delete_product(product_id):
    
    # Permitido leitura acessando diretamente a API
    p = db.session.get(Product, product_id)
    if not p:
        return {"error": "Produto não encontrado"}, 404
    data = request.get_json() or {}
    message = {"op": "delete", "data": {"id": product_id}}
    r = _get_redis()
    r.lpush(current_app.config.get('PRODUCT_QUEUE', 'product_queue'), json.dumps(message))
    return {"message": "enqueued"}, 202
    