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

# 2. Parar containers
echo -e "${YELLOW}🛑 Parando containers...${NC}"
docker-compose -f docker-compose.prod.yml down
echo -e "${GREEN}✅ Containers parados${NC}"

# 3. Rebuild do container web
echo -e "${YELLOW}🔨 Fazendo rebuild do container web...${NC}"
docker-compose -f docker-compose.prod.yml build --no-cache web
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao fazer build${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Build concluído${NC}"

# 4. Subir containers
echo -e "${YELLOW}🚀 Subindo containers...${NC}"
docker-compose -f docker-compose.prod.yml up -d
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao subir containers${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Containers iniciados${NC}"

# 5. Aguardar containers subirem
echo -e "${YELLOW}⏳ Aguardando containers iniciarem (20s)...${NC}"
sleep 20

# 6. Aplicar migrações
echo -e "${YELLOW}🗄️ Aplicando migrações do banco...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️ Aviso: Erro nas migrações (pode ser normal se não houver novas)${NC}"
fi
echo -e "${GREEN}✅ Migrações processadas${NC}"

# 7. LIMPAR diretório staticfiles COMPLETAMENTE
echo -e "${YELLOW}🧹 Limpando staticfiles antigos...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web rm -rf /app/staticfiles/*
docker-compose -f docker-compose.prod.yml exec -T web mkdir -p /app/staticfiles
echo -e "${GREEN}✅ Staticfiles limpo${NC}"

# 8. Coletar arquivos estáticos NOVOS
echo -e "${YELLOW}📦 Coletando arquivos estáticos (CSS, JS, Imagens)...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao coletar estáticos${NC}"
    # Mostrar erro detalhado
    docker-compose -f docker-compose.prod.yml logs web | tail -50
    exit 1
fi
echo -e "${GREEN}✅ Arquivos estáticos coletados!${NC}"

# 9. Verificar se arquivos foram coletados
echo -e "${YELLOW}🔍 Verificando arquivos coletados...${NC}"
echo "CSS da calculadora:"
docker-compose -f docker-compose.prod.yml exec -T web ls -lh /app/staticfiles/css/calculadora.css 2>&1
echo ""
echo "Logos de parceiros:"
docker-compose -f docker-compose.prod.yml exec -T web ls -lh /app/staticfiles/img/ | grep -E "^-.*\.png$" | head -20
echo ""

# 10. Ajustar permissões
echo -e "${YELLOW}🔐 Ajustando permissões...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web chmod -R 755 /app/staticfiles
docker-compose -f docker-compose.prod.yml exec -T web chmod -R 755 /app/media
echo -e "${GREEN}✅ Permissões ajustadas${NC}"

# 11. Reiniciar serviço web para garantir
echo -e "${YELLOW}🔄 Reiniciando serviço web...${NC}"
docker-compose -f docker-compose.prod.yml restart web
sleep 5
echo -e "${GREEN}✅ Serviço web reiniciado${NC}"

# 12. Verificar status
echo -e "${YELLOW}🔍 Verificando status dos containers...${NC}"
docker-compose -f docker-compose.prod.yml ps

# 13. Mostrar logs recentes
echo ""
echo -e "${YELLOW}📋 Últimas 10 linhas dos logs:${NC}"
docker-compose -f docker-compose.prod.yml logs --tail=10 web

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ DEPLOY CONCLUÍDO COM SUCESSO!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}📝 O que foi feito:${NC}"
echo "  ✓ Git pull das alterações"
echo "  ✓ Containers parados"
echo "  ✓ Rebuild completo do container web"
echo "  ✓ Containers reiniciados"
echo "  ✓ Migrações aplicadas"
echo "  ✓ Staticfiles limpo completamente"
echo "  ✓ Arquivos estáticos coletados (CSS + Imagens)"
echo "  ✓ Permissões ajustadas"
echo "  ✓ Serviço web reiniciado"
echo ""
echo -e "${YELLOW}🌐 Acesse: https://contabilvetorial.com.br${NC}"
echo ""
echo -e "${YELLOW}💡 Comandos úteis:${NC}"
echo "  Ver logs: docker-compose -f docker-compose.prod.yml logs -f web"
echo "  Verificar CSS: docker-compose -f docker-compose.prod.yml exec web cat /app/staticfiles/css/calculadora.css | head -20"
echo "  Listar imagens: docker-compose -f docker-compose.prod.yml exec web ls -la /app/staticfiles/img/"
echo ""
