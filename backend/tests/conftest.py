import pytest
import sys
from pathlib import Path

# Adicionar o diretório backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.database import db
from app.models.user import User
from app.models.product import Product

@pytest.fixture
def app():
    """Criar aplicação Flask para testes"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente HTTP para fazer requests"""
    return app.test_client()

@pytest.fixture
def auth_headers(client, app):
    """Headers com token JWT válido"""
    # Criar usuário de teste
    with app.app_context():
        from app.services.auth_service import register_user
        register_user('testuser', 'testpass123')
    
    # Fazer login
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}