#!/bin/bash

# Script de Deploy com Otimizações de Performance
# Executar no servidor de produção

set -e  # Parar em caso de erro

echo "======================================"
echo "🚀 Deploy Vetorial - Performance Mode"
echo "======================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório do projeto
PROJECT_DIR="/root/vetorial"
cd $PROJECT_DIR

echo ""
echo "${YELLOW}1. Fazendo backup do banco de dados...${NC}"
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres gestao360_db > backup_$(date +%Y%m%d_%H%M%S).sql
echo "${GREEN}✓ Backup criado${NC}"

echo ""
echo "${YELLOW}2. Puxando alterações do Git...${NC}"
git pull origin master
echo "${GREEN}✓ Código atualizado${NC}"

echo ""
echo "${YELLOW}3. Instalando dependências Python...${NC}"
docker-compose -f docker-compose.prod.yml exec web pip install -r requirements.txt --no-cache-dir
echo "${GREEN}✓ Dependências instaladas${NC}"

echo ""
echo "${YELLOW}4. Executando migrações do banco...${NC}"
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
echo "${GREEN}✓ Migrações aplicadas${NC}"

echo ""
echo "${YELLOW}5. Coletando arquivos estáticos (com compressão)...${NC}"
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput --clear
echo "${GREEN}✓ Arquivos estáticos coletados${NC}"

echo ""
echo "${YELLOW}6. Copiando arquivos estáticos para o host...${NC}"
docker cp vetorial_web:/app/staticfiles/. $PROJECT_DIR/staticfiles/
chmod -R 755 $PROJECT_DIR/staticfiles/
echo "${GREEN}✓ Arquivos copiados${NC}"

echo ""
echo "${YELLOW}7. Ajustando permissões de media...${NC}"
chmod -R 755 $PROJECT_DIR/media/
echo "${GREEN}✓ Permissões ajustadas${NC}"

echo ""
echo "${YELLOW}8. Limpando cache do Redis...${NC}"
docker-compose -f docker-compose.prod.yml exec redis redis-cli FLUSHDB
echo "${GREEN}✓ Cache limpo${NC}"

echo ""
echo "${YELLOW}9. Reiniciando serviços...${NC}"
docker-compose -f docker-compose.prod.yml restart web
docker-compose -f docker-compose.prod.yml restart celery_worker
docker-compose -f docker-compose.prod.yml restart celery_beat
echo "${GREEN}✓ Serviços reiniciados${NC}"

echo ""
echo "${YELLOW}10. Testando Nginx...${NC}"
nginx -t
if [ $? -eq 0 ]; then
    echo "${GREEN}✓ Configuração do Nginx OK${NC}"
    echo "${YELLOW}11. Recarregando Nginx...${NC}"
    systemctl reload nginx
    echo "${GREEN}✓ Nginx recarregado${NC}"
else
    echo "${RED}✗ Erro na configuração do Nginx${NC}"
    exit 1
fi

echo ""
echo "${YELLOW}12. Verificando status dos containers...${NC}"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "${YELLOW}13. Verificando logs recentes...${NC}"
docker-compose -f docker-compose.prod.yml logs --tail=20 web

echo ""
echo "======================================"
echo "${GREEN}✓ Deploy concluído com sucesso!${NC}"
echo "======================================"
echo ""
echo "📊 Próximos passos:"
echo "1. Testar o site: https://contabilvetorial.com.br"
echo "2. Verificar performance: https://pagespeed.web.dev/"
echo "3. Monitorar logs: docker-compose -f docker-compose.prod.yml logs -f web"
echo ""
echo "🔍 Comandos úteis:"
echo "  - Ver logs: docker-compose -f docker-compose.prod.yml logs -f [service]"
echo "  - Status: docker-compose -f docker-compose.prod.yml ps"
echo "  - Cache Redis: docker-compose -f docker-compose.prod.yml exec redis redis-cli INFO stats"
echo ""
