import pytest

def test_register_success(client):
    """Teste: Registrar novo usuário com sucesso"""
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'newuser'
    assert 'id' in data

def test_register_duplicate_username(client):
    """Teste: Tentar registrar username duplicado"""
    # Primeiro registro
    client.post('/auth/register', json={
        'username': 'duplicate',
        'password': 'pass123'
    })
    
    # Segundo registro (falha)
    response = client.post('/auth/register', json={
        'username': 'duplicate',
        'password': 'pass123'
    })
    
    assert response.status_code == 400
    assert 'username_already_exists' in response.get_json()['message']

def test_register_missing_fields(client):
    """Teste: Registrar sem campos obrigatórios"""
    response = client.post('/auth/register', json={
        'username': 'onlyusername'
    })
    
    assert response.status_code == 400

def test_login_success(client):
    """Teste: Login com credenciais corretas"""
    # Registrar usuário
    client.post('/auth/register', json={
        'username': 'loginuser',
        'password': 'loginpass'
    })
    
    # Fazer login
    response = client.post('/auth/login', json={
        'username': 'loginuser',
        'password': 'loginpass'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data

def test_login_wrong_password(client):
    """Teste: Login com senha errada"""
    # Registrar usuário
    client.post('/auth/register', json={
        'username': 'user1',
        'password': 'correctpass'
    })
    
    # Tentar login com senha errada
    response = client.post('/auth/login', json={
        'username': 'user1',
        'password': 'wrongpass'
    })
    
    assert response.status_code == 401
    assert 'credenciais inválidas' in response.get_json()['message']

def test_login_user_not_exists(client):
    """Teste: Login com usuário inexistente"""
    response = client.post('/auth/login', json={
        'username': 'nonexistent',
        'password': 'anypass'
    })
    
    assert response.status_code == 401

def test_me_endpoint_authenticated(client, auth_headers):
    """Teste: Acessar /me com token válido"""
    response = client.get('/auth/me', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'user_id' in data

def test_me_endpoint_unauthenticated(client):
    """Teste: Acessar /me sem token"""
    response = client.get('/auth/me')
    
    assert response.status_code == 401