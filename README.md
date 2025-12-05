# 🦈 Shark Gaming - Sistema de Gerenciamento de Produtos

Sistema web completo para gerenciamento de produtos de periféricos gamers, desenvolvido com **Flask** (backend) e **Angular 19** (frontend), utilizando arquitetura de filas com **Redis** para processamento assíncrono.

---

## 📋 Índice

- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
- [Executando o Projeto](#executando-o-projeto)
- [Testes](#testes)
- [Documentação da API (Swagger)](#documentação-da-api-swagger)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)

---

## 🚀 Tecnologias

### Backend
- **Python 3.12**
- **Flask** - Framework web
- **Flask-JWT-Extended** - Autenticação JWT
- **SQLAlchemy** - ORM
- **PostgreSQL** - Banco de dados
- **Redis** - Fila de mensagens
- **Flask-RESTX** - Documentação Swagger
- **Pytest** - Testes automatizados

### Frontend
- **Angular 19** - Framework frontend
- **TypeScript**
- **Angular Router** - Navegação
- **HTTP Interceptors** - Middleware de requisições

### DevOps
- **Docker & Docker Compose** - Containerização

---

## 🏗️ Arquitetura

![Arquitetura](docs/arquitetura-shark.png)

**Fluxo de operações:**
1. Frontend envia requisição para API
2. API autentica com JWT
3. Operações de escrita (CREATE/UPDATE/DELETE) são enfileiradas no Redis
4. Worker consome a fila e processa no banco de dados
5. Operações de leitura (GET) são síncronas

---

## 📦 Pré-requisitos

### Obrigatórios
- **Python 3.12+**
- **Node.js 18+** e **npm**
- **PostgreSQL 12+**
- **Docker** e **Docker Compose** (para Redis)

### Verificar instalação

```bash
python --version   # Python 3.12.3 ou superior
node --version     # v18.x.x ou superior
npm --version      # 9.x.x ou superior
psql --version     # PostgreSQL 14.x ou superior
docker --version   # Docker 20.x.x ou superior
```

---

## 📥 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/shark-gaming.git
cd shark-gaming
```

### 2. Configurar Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependências
npm install
```

---

## 🗄️ Configuração do Banco de Dados

### 1. Criar banco de dados PostgreSQL

```sql
-- Conectar ao PostgreSQL
psql -U postgres

-- Criar banco de dados
CREATE DATABASE techsolutions;

-- Conectar ao banco
\c techsolutions

-- Criar tabelas (serão criadas automaticamente pelo Flask)
```

### 2. Configurar variáveis de ambiente (caso queira alterar)

Criar arquivo `.env` em `backend/app/.env`:

```env
# Banco de Dados
DATABASE_URL=postgresql://postgres:SUA_SENHA@host.docker.internal:5432/techsolutions

# JWT Secret (gere uma chave segura)
JWT_SECRET_KEY=sua_chave_secreta_muito_segura_aqui

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
PRODUCT_QUEUE=product_queue
```

**⚠️ IMPORTANTE:** Substitua `SUA_SENHA` pela senha do seu PostgreSQL local.

### 3. Gerar JWT Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado e cole em `JWT_SECRET_KEY` no arquivo `.env`.

---

## ▶️ Executando o Projeto

### Opção 1: Com Docker (Recomendado)

```bash
# Na raiz do projeto
docker-compose up --build
```

**Serviços iniciados:**
- Backend (Flask): http://localhost:5000
- Frontend (Angular): http://localhost:4200
- Worker: Processamento assíncrono
- Redis: localhost:6379

### Opção 2: Sem Docker (Manual)

#### Terminal 1 - Iniciar Redis
```bash
# Windows (com Chocolatey):
choco install redis
redis-server

# Linux:
sudo systemctl start redis

# Mac:
brew services start redis
```

#### Terminal 2 - Iniciar Backend
```bash
cd backend
python run.py
```

#### Terminal 3 - Iniciar Worker
```bash
cd backend
python worker.py
```

#### Terminal 4 - Iniciar Frontend
```bash
cd frontend
npm start
```

**Acessar aplicação:**
- Frontend: http://localhost:4200
- Backend API: http://localhost:5000

---

## 🧪 Testes

### Executar testes automatizados

```bash
cd backend

# Instalar dependências de teste
pip install pytest pytest-flask pytest-cov

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app --cov-report=html

# Executar testes específicos
pytest tests/test_auth.py

# Ver relatório de cobertura
# Abrir: htmlcov/index.html no navegador
```

### Testes disponíveis

**Autenticação (`test_auth.py`):**
- ✅ Registro de usuário
- ✅ Login com credenciais corretas/incorretas
- ✅ Validação de token JWT
- ✅ Endpoint protegido `/me`

---

## 📚 Documentação da API (Swagger)

### Acessar Swagger UI

```
http://localhost:5000/api/docs
```

### Testar endpoints com autenticação

1. **Registrar usuário** via `/auth/register`
2. **Fazer login** via `/auth/login` → Copiar o `access_token`
3. **Clicar em "Authorize"** no Swagger UI
4. **Colar token** no formato: `Bearer <seu_token>`
5. **Testar endpoints** protegidos

### OpenAPI Specification

```
http://localhost:5000/api/swagger.json
```

---

## 📁 Estrutura do Projeto

```
shark-gaming-store/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Factory da aplicação Flask
│   │   ├── config.py            # Configurações (JWT, Redis, DB)
│   │   ├── database.py          # Instância do SQLAlchemy
│   │   ├── models/
│   │   │   ├── user.py          # Modelo User
│   │   │   └── product.py       # Modelo Product
│   │   ├── routes/
│   │   │   ├── auth.py          # Rotas de autenticação
│   │   │   ├── products.py      # Rotas de produtos
│   │   │   └── swagger_docs.py  # Documentação Swagger
│   │   └── services/
│   │       ├── auth_service.py  # Lógica de autenticação
│   │       └── product_service.py
│   ├── tests/
│   │   ├── conftest.py          # Fixtures do Pytest
│   │   ├── test_auth.py         # Testes de autenticação
│   ├── requirements.txt
│   ├── run.py                   # Entry point da API
│   ├── worker.py                # Worker do Redis
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── home/        # Página inicial
│   │   │   │   ├── login/       # Tela de login
│   │   │   │   ├── register/    # Tela de cadastro
│   │   │   │   └── products/    # CRUD de produtos
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts    # Proteção de rotas
│   │   │   ├── interceptors/
│   │   │   │   └── auth.interceptor.ts  # Intercepta erros 401/422
│   │   │   ├── models/
│   │   │   │   ├── user.model.ts
│   │   │   │   └── product.model.ts
│   │   │   ├── services/
│   │   │   │   ├── auth.service.ts     # Serviço de autenticação
│   │   │   │   └── product.service.ts  # Serviço de produtos
│   │   │   ├── app.module.ts
│   │   │   ├── app-routing.module.ts
│   │   │   └── app.component.ts
│   │   ├── styles.css
│   │   └── main.ts
│   ├── package.json
│   ├── angular.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ✨ Funcionalidades

### 🔐 Autenticação
- Registro de usuários
- Login com JWT
- Proteção de rotas
- Auto-logout em token expirado (30 minutos)
- Redirecionamento inteligente após login

### 📦 Gerenciamento de Produtos
- ✅ **Listar** produtos (tempo real)
- ➕ **Criar** produto (assíncrono via Redis)
- ✏️ **Editar** produto (assíncrono via Redis)
- 🗑️ **Deletar** produto (assíncrono via Redis)
- 🔍 **Validações** de campos obrigatórios

### 🎨 Interface
- Design moderno e responsivo
- Feedback visual de operações
- Mensagens de sucesso/erro
- Navegação fluída
- Logo clicável (volta para home)
- Menu contextual (Login/Sair)

---

## 🔧 Configurações Avançadas

### Alterar tempo de expiração do token

```python
# backend/app/config.py
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)  # Alterar aqui
```

### Configurar CORS para produção

```python
# backend/app/__init__.py
CORS(app, resources={
    r"/*": {
        "origins": ["https://seudominio.com"],  # Domínio de produção
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Build de produção (Angular)

```bash
cd frontend
npm run build

# Arquivos gerados em: dist/frontend
# Servir com Nginx ou similar
```

---

## 🐛 Troubleshooting

### Erro: "Connection refused" no PostgreSQL
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql  # Linux
# Verificar porta 5432
netstat -an | grep 5432
```

### Erro: "Redis connection failed"
```bash
# Verificar se Redis está rodando
redis-cli ping
# Deve retornar: PONG
```

---

## 📝 Licença

Este projeto é de uso demonstrativo.

**Desenvolvido por um gamer para gamers** 🦈🎮
