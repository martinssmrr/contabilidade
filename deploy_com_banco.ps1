# Script PowerShell para enviar backup e restaurar na VPS

$VPS_IP = "contabilvetorial.com.br"
$VPS_USER = "root"
$VPS_PATH = "/root/vetorial"

Write-Host "=========================================="
Write-Host "DEPLOY COM BANCO DE DADOS - VPS PRODUÇÃO"
Write-Host "=========================================="
Write-Host ""

# 1. Verificar se o backup existe
if (-not (Test-Path "backup_banco.sql")) {
    Write-Host "❌ Erro: backup_banco.sql não encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: docker-compose exec -T db pg_dump -U postgres gestao360_db > backup_banco.sql"
    exit 1
}

Write-Host "✅ Backup encontrado: backup_banco.sql" -ForegroundColor Green
Write-Host ""

# 2. Fazer commit das alterações
Write-Host "1. Fazendo commit das alterações locais..." -ForegroundColor Cyan
git add .
git commit -m "Atualização com CKEditor 5 e dados atualizados"
git push origin master

Write-Host ""
Write-Host "2. Enviando backup do banco para VPS..." -ForegroundColor Cyan
scp backup_banco.sql "${VPS_USER}@${VPS_IP}:${VPS_PATH}/"

Write-Host ""
Write-Host "3. Enviando script de restauração..." -ForegroundColor Cyan
scp restaurar_banco_producao.sh "${VPS_USER}@${VPS_IP}:${VPS_PATH}/"

Write-Host ""
Write-Host "4. Conectando na VPS para executar deploy..." -ForegroundColor Cyan
Write-Host ""

# 3. Executar comandos na VPS
$comandos = @"
cd /root/vetorial
git pull origin master
chmod +x restaurar_banco_producao.sh
./restaurar_banco_producao.sh
"@

ssh "${VPS_USER}@${VPS_IP}" $comandos

Write-Host ""
Write-Host "✅ Deploy concluído com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Site: http://contabilvetorial.com.br" -ForegroundColor Yellow
Write-Host "🔐 Admin: http://contabilvetorial.com.br/admin/" -ForegroundColor Yellow
