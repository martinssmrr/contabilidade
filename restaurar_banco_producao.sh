#!/bin/bash
# Script para restaurar o banco de dados na VPS de produção

echo "=========================================="
echo "RESTAURAÇÃO DO BANCO DE DADOS - PRODUÇÃO"
echo "=========================================="
echo ""

# Verificar se o arquivo backup_banco.sql existe
if [ ! -f "backup_banco.sql" ]; then
    echo "❌ Erro: arquivo backup_banco.sql não encontrado!"
    echo "Faça o upload do arquivo primeiro usando SCP ou FTP"
    exit 1
fi

echo "⚠️  ATENÇÃO: Este script vai SUBSTITUIR todos os dados do banco de produção!"
echo "Pressione Ctrl+C para cancelar ou Enter para continuar..."
read

echo ""
echo "1. Parando containers..."
docker-compose -f docker-compose.prod.yml down

echo ""
echo "2. Removendo banco antigo..."
docker volume rm vetorial_postgres_data 2>/dev/null || true

echo ""
echo "3. Iniciando apenas o banco de dados..."
docker-compose -f docker-compose.prod.yml up -d db

echo ""
echo "4. Aguardando banco inicializar (15 segundos)..."
sleep 15

echo ""
echo "5. Restaurando backup..."
cat backup_banco.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres -d gestao360_db

echo ""
echo "6. Iniciando aplicação web..."
docker-compose -f docker-compose.prod.yml up -d web

echo ""
echo "7. Coletando arquivos estáticos..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

echo ""
echo "8. Verificando status dos containers..."
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "✅ Restauração concluída!"
echo ""
echo "Acesse: http://vetorialcontabilidade.com.br"
echo "Admin: http://vetorialcontabilidade.com.br/admin/"
