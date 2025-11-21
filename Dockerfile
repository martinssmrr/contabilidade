# ==================================
# DOCKERFILE PARA O PROJETO GESTÃO 360
# ==================================

# Usa a imagem oficial do Python 3.11 como base
FROM python:3.11-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para o PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requirements e instala as dependências Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o container
COPY . /app/

# Cria diretórios para static e media
RUN mkdir -p /app/staticfiles /app/media

# Expõe a porta 8000 para o servidor Django
EXPOSE 8000

# Comando para executar a aplicação
# Em produção, substitua por gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
