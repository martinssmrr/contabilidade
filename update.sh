#!/bin/bash

# ==================================
# ATUALIZAÇÃO RÁPIDA - VETORIAL
# ==================================

echo "Atualizando aplicação Vetorial..."

cd /var/www/vetorial

# Pull do código
echo "1. Baixando atualizações..."
sudo -u vetorial git pull origin main

# Atualizar dependências
echo "2. Atualizando dependências..."
sudo -u vetorial venv/bin/pip install -r requirements.txt

# Executar migrações
echo "3. Executando migrações..."
sudo -u vetorial venv/bin/python manage.py migrate

# Coletar arquivos estáticos
echo "4. Coletando arquivos estáticos..."
sudo -u vetorial venv/bin/python manage.py collectstatic --noinput

# Reiniciar Gunicorn
echo "5. Reiniciando aplicação..."
sudo systemctl restart gunicorn-vetorial

# Verificar status
echo "6. Verificando status..."
sudo systemctl status gunicorn-vetorial --no-pager

echo "====================================="
echo "ATUALIZAÇÃO CONCLUÍDA!"
echo "====================================="
