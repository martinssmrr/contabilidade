#!/bin/bash

# ==================================
# SCRIPT DE DEPLOY - VETORIAL (DOCKER)
# Deploy na VPS Hostinger com Docker
# Domínio: contabilvetorial.com.br
# ==================================

echo "====================================="
echo "DEPLOY VETORIAL - Hostinger VPS (Docker)"
echo "====================================="

# Atualizar sistema
echo "1. Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar Docker e Docker Compose
echo "2. Instalando Docker e Docker Compose..."
sudo apt install -y docker.io docker-compose git curl

# Habilitar Docker no boot
echo "3. Configurando Docker..."
sudo systemctl enable docker
sudo systemctl start docker

# Adicionar usuário atual ao grupo docker
sudo usermod -aG docker $USER

# Criar diretório do projeto
echo "4. Criando estrutura de diretórios..."
sudo mkdir -p /var/www/vetorial
cd /var/www/vetorial

# Clonar ou copiar projeto
echo "5. Configurando projeto..."
# Se estiver usando git:
# git clone seu-repositorio-git .
# Ou copie os arquivos manualmente para /var/www/vetorial

# Criar arquivo .env
echo "6. Criando arquivo .env..."
cat > /var/www/vetorial/.env << 'EOF'
# Django
SECRET_KEY=GERE_UMA_SECRET_KEY_SEGURA_AQUI
DEBUG=False
ALLOWED_HOSTS=contabilvetorial.com.br,www.contabilvetorial.com.br

# Database
DB_NAME=vetorial_db
DB_USER=vetorial_user
DB_PASSWORD=SENHA_SEGURA_DO_BANCO_AQUI
DB_HOST=db
DB_PORT=5432

# Mercado Pago
MP_PUBLIC_KEY=sua-public-key
MP_ACCESS_TOKEN=seu-access-token
EOF

echo "⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais reais!"
echo "Execute: nano /var/www/vetorial/.env"
read -p "Pressione ENTER depois de editar o .env..."

# Criar diretório para backups
echo "7. Criando diretório de backups..."
mkdir -p /var/www/vetorial/backups

# Build das imagens Docker
echo "8. Construindo imagens Docker..."
docker-compose -f docker-compose.prod.yml build

# Iniciar containers
echo "9. Iniciando containers..."
docker-compose -f docker-compose.prod.yml up -d

# Aguardar containers iniciarem
echo "10. Aguardando containers iniciarem..."
sleep 10

# Executar migrações
echo "11. Executando migrações..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate

# Criar superusuário
echo "12. Criar superusuário Django..."
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Popular CNAEs
echo "13. Populando CNAEs..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py popular_cnaes || echo "Comando não encontrado, pulando..."

# Configurar SSL com Certbot
echo "14. Configurando SSL Certificate..."
echo "Primeiro vamos obter o certificado SSL..."

# Parar nginx temporariamente
docker-compose -f docker-compose.prod.yml stop nginx

# Obter certificado SSL
docker run -it --rm \
  -v /var/www/vetorial/nginx/ssl:/etc/letsencrypt \
  -v /var/www/vetorial/certbot:/var/www/certbot \
  -p 80:80 \
  certbot/certbot certonly \
  --standalone \
  --email seu-email@exemplo.com \
  --agree-tos \
  --no-eff-email \
  -d contabilvetorial.com.br \
  -d www.contabilvetorial.com.br

# Reiniciar nginx
docker-compose -f docker-compose.prod.yml start nginx

# Configurar renovação automática SSL (cron)
echo "15. Configurando renovação automática SSL..."
(crontab -l 2>/dev/null; echo "0 3 * * * cd /var/www/vetorial && docker-compose -f docker-compose.prod.yml run --rm certbot renew && docker-compose -f docker-compose.prod.yml restart nginx") | crontab -

# Configurar backup automático (cron)
echo "16. Configurando backup automático..."
chmod +x /var/www/vetorial/backup-docker.sh
(crontab -l 2>/dev/null; echo "0 2 * * * /var/www/vetorial/backup-docker.sh") | crontab -

echo "====================================="
echo "DEPLOY CONCLUÍDO!"
echo "====================================="
echo "Seu site está disponível em:"
echo "https://contabilvetorial.com.br"
echo ""
echo "Comandos úteis Docker:"
echo "- Ver logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "- Ver logs web: docker-compose -f docker-compose.prod.yml logs -f web"
echo "- Reiniciar: docker-compose -f docker-compose.prod.yml restart"
echo "- Parar: docker-compose -f docker-compose.prod.yml down"
echo "- Status: docker-compose -f docker-compose.prod.yml ps"
echo ""
echo "Comandos Django:"
echo "- Shell: docker-compose -f docker-compose.prod.yml exec web python manage.py shell"
echo "- Migrações: docker-compose -f docker-compose.prod.yml exec web python manage.py migrate"
echo "- Collectstatic: docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic"
echo "====================================="
