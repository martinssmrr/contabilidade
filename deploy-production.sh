#!/bin/bash

# ==================================
# SCRIPT DE DEPLOY PARA PRODUÇÃO
# Vetorial - contabilvetorial.com.br
# ==================================

echo "🚀 Iniciando deploy em produção..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Pull das alterações
echo -e "${YELLOW}📥 Baixando últimas alterações do Git...${NC}"
git pull origin master
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao fazer git pull${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Git pull concluído${NC}"

# 2. Rebuild dos containers (se necessário)
echo -e "${YELLOW}🔨 Verificando se precisa rebuild...${NC}"
docker-compose -f docker-compose.prod.yml build --no-cache web
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao fazer build${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Build concluído${NC}"

# 3. Reiniciar containers
echo -e "${YELLOW}🔄 Reiniciando containers...${NC}"
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao reiniciar containers${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Containers reiniciados${NC}"

# Aguardar containers subirem
echo -e "${YELLOW}⏳ Aguardando containers iniciarem (15s)...${NC}"
sleep 15

# 4. Aplicar migrações
echo -e "${YELLOW}🗄️ Aplicando migrações do banco...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao aplicar migrações${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Migrações aplicadas${NC}"

# 5. Coletar arquivos estáticos (IMPORTANTE!)
echo -e "${YELLOW}📦 Coletando arquivos estáticos (CSS, JS, Imagens)...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput --clear
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao coletar estáticos${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Arquivos estáticos coletados com sucesso!${NC}"

# 6. Verificar permissões dos estáticos
echo -e "${YELLOW}🔐 Ajustando permissões...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web chmod -R 755 /app/staticfiles
docker-compose -f docker-compose.prod.yml exec -T web chmod -R 755 /app/media
echo -e "${GREEN}✅ Permissões ajustadas${NC}"

# 7. Reiniciar serviço web final
echo -e "${YELLOW}🔄 Reiniciando serviço web...${NC}"
docker-compose -f docker-compose.prod.yml restart web
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao reiniciar web${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Serviço web reiniciado${NC}"

# 8. Verificar status
echo -e "${YELLOW}🔍 Verificando status dos containers...${NC}"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ DEPLOY CONCLUÍDO COM SUCESSO!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}📝 O que foi feito:${NC}"
echo "  ✓ Git pull das alterações"
echo "  ✓ Rebuild do container web"
echo "  ✓ Reinício dos containers"
echo "  ✓ Migrações aplicadas"
echo "  ✓ Arquivos estáticos coletados (CSS da calculadora + logos)"
echo "  ✓ Permissões ajustadas"
echo "  ✓ Serviço web reiniciado"
echo ""
echo -e "${YELLOW}🌐 Acesse: https://contabilvetorial.com.br${NC}"
echo ""
echo -e "${YELLOW}💡 Para ver logs em tempo real:${NC}"
echo "  docker-compose -f docker-compose.prod.yml logs -f web"
echo ""
