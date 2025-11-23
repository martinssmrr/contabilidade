#!/bin/bash

# ==================================
# ATUALIZAÇÃO RÁPIDA - VETORIAL (DOCKER)
# ==================================

echo "Atualizando aplicação Vetorial (Docker)..."

cd /var/www/vetorial

# Pull do código
echo "1. Baixando atualizações..."
git pull origin main

# Rebuild das imagens
echo "2. Reconstruindo imagens..."
docker-compose -f docker-compose.prod.yml build

# Parar containers
echo "3. Parando containers..."
docker-compose -f docker-compose.prod.yml down

# Iniciar containers atualizados
echo "4. Iniciando containers atualizados..."
docker-compose -f docker-compose.prod.yml up -d

# Aguardar containers iniciarem
sleep 10

# Executar migrações
echo "5. Executando migrações..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate

# Coletar arquivos estáticos
echo "6. Coletando arquivos estáticos..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

# Verificar status
echo "7. Verificando status..."
docker-compose -f docker-compose.prod.yml ps

echo "====================================="
echo "ATUALIZAÇÃO CONCLUÍDA!"
echo "====================================="
