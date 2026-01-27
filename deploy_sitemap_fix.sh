#!/bin/bash
# Script de deploy para correções de sitemap
# Execute via SSH no servidor

echo "=== Deploy: Correção do Sitemap ==="
echo ""

echo "1. Navegando para o diretório do projeto..."
cd /root/contabilidade || exit 1

echo "2. Fazendo pull das alterações..."
git pull origin master

echo "3. Reiniciando o container web..."
docker-compose -f docker-compose.prod.yml restart web

echo "4. Aguardando container iniciar..."
sleep 5

echo "5. Verificando status dos containers..."
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "=== Deploy concluído! ==="
echo ""
echo "Teste o sitemap em: https://vetorialcontabilidade.com.br/sitemap.xml"
echo ""
