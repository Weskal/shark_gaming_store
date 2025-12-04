FROM python:3.12.3-slim

WORKDIR /app

# Instalar gcc para compilar dependências Python
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Expor porta
EXPOSE 5000

# Comando para rodar
CMD ["python", "run.py"]