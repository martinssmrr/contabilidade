#!/bin/bash

# ==================================
# BACKUP DO BANCO DE DADOS - DOCKER
# ==================================

BACKUP_DIR="/var/www/vetorial/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_${DATE}.sql"

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Fazer backup usando Docker
echo "Fazendo backup do banco de dados..."
docker-compose -f /var/www/vetorial/docker-compose.prod.yml exec -T db \
  pg_dump -U vetorial_user vetorial_db > $BACKUP_FILE

# Comprimir backup
echo "Comprimindo backup..."
gzip $BACKUP_FILE

echo "Backup salvo em: ${BACKUP_FILE}.gz"

# Manter apenas os últimos 7 backups
echo "Removendo backups antigos..."
ls -t $BACKUP_DIR/backup_*.sql.gz | tail -n +8 | xargs -r rm

echo "Backup concluído!"
