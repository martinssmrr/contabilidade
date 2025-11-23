#!/bin/bash

# ==================================
# BACKUP DO BANCO DE DADOS - VETORIAL
# ==================================

# Configurações
BACKUP_DIR="/var/www/vetorial/backups"
DB_NAME="vetorial_db"
DB_USER="vetorial_user"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_${DATE}.sql"

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Fazer backup
echo "Fazendo backup do banco de dados..."
sudo -u postgres pg_dump $DB_NAME > $BACKUP_FILE

# Comprimir backup
echo "Comprimindo backup..."
gzip $BACKUP_FILE

echo "Backup salvo em: ${BACKUP_FILE}.gz"

# Manter apenas os últimos 7 backups
echo "Removendo backups antigos..."
ls -t $BACKUP_DIR/backup_*.sql.gz | tail -n +8 | xargs -r rm

echo "Backup concluído!"
