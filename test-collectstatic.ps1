# ============================================
# SCRIPT DE TESTE LOCAL - VETORIAL
# Verifica se collectstatic funciona localmente
# ============================================

Write-Host "🧪 Testando coleta de estáticos localmente..." -ForegroundColor Yellow
Write-Host ""

# 1. Verificar se arquivos existem
Write-Host "📁 Verificando arquivos no diretório static/..." -ForegroundColor Cyan

$calcCSS = "static\css\calculadora.css"
if (Test-Path $calcCSS) {
    $size = (Get-Item $calcCSS).Length
    Write-Host "  ✅ calculadora.css encontrado ($size bytes)" -ForegroundColor Green
} else {
    Write-Host "  ❌ calculadora.css NÃO encontrado!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Verificando logos em static/img/..." -ForegroundColor Cyan
$logos = Get-ChildItem "static\img\*.png" | Where-Object { $_.Name -match '^\d+\.png$' } | Sort-Object { [int]($_.BaseName) }
Write-Host "  ✅ Encontradas $($logos.Count) logos numeradas:" -ForegroundColor Green
$logos | ForEach-Object { Write-Host "    - $($_.Name)" -ForegroundColor Gray }

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow

# 2. Limpar staticfiles antigo
Write-Host ""
Write-Host "🧹 Limpando staticfiles antigos..." -ForegroundColor Cyan
if (Test-Path "staticfiles") {
    Remove-Item "staticfiles" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  ✅ Staticfiles limpo" -ForegroundColor Green
}

# 3. Testar collectstatic
Write-Host ""
Write-Host "📦 Executando collectstatic..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

python manage.py collectstatic --noinput --clear

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Collectstatic executado com sucesso!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ ERRO ao executar collectstatic!" -ForegroundColor Red
    Write-Host "Verifique os logs acima para detalhes." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow

# 4. Verificar se arquivos foram coletados
Write-Host ""
Write-Host "🔍 Verificando arquivos coletados em staticfiles/..." -ForegroundColor Cyan

$collectedCSS = "staticfiles\css\calculadora.css"
if (Test-Path $collectedCSS) {
    $size = (Get-Item $collectedCSS).Length
    Write-Host "  ✅ calculadora.css coletado ($size bytes)" -ForegroundColor Green
} else {
    Write-Host "  ❌ calculadora.css NÃO foi coletado!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Verificando logos em staticfiles/img/..." -ForegroundColor Cyan
$collectedLogos = Get-ChildItem "staticfiles\img\*.png" -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^\d+\.png$' } | Sort-Object { [int]($_.BaseName) }
if ($collectedLogos) {
    Write-Host "  ✅ $($collectedLogos.Count) logos coletadas:" -ForegroundColor Green
    $collectedLogos | ForEach-Object { Write-Host "    - $($_.Name)" -ForegroundColor Gray }
} else {
    Write-Host "  ❌ Nenhuma logo foi coletada!" -ForegroundColor Red
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow

# 5. Resumo final
Write-Host ""
Write-Host "📊 RESUMO DO TESTE" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow

if ((Test-Path $collectedCSS) -and $collectedLogos) {
    Write-Host "✅ TESTE PASSOU!" -ForegroundColor Green
    Write-Host "Todos os arquivos foram coletados corretamente." -ForegroundColor Green
    Write-Host ""
    Write-Host "Próximos passos:" -ForegroundColor Yellow
    Write-Host "  1. Fazer commit e push das alterações:" -ForegroundColor White
    Write-Host "     git add ." -ForegroundColor Gray
    Write-Host "     git commit -m 'fix: corrige STATIC_URL e configuração WhiteNoise'" -ForegroundColor Gray
    Write-Host "     git push origin master" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. No servidor, executar:" -ForegroundColor White
    Write-Host "     chmod +x deploy-production.sh" -ForegroundColor Gray
    Write-Host "     ./deploy-production.sh" -ForegroundColor Gray
} else {
    Write-Host "❌ TESTE FALHOU!" -ForegroundColor Red
    Write-Host "Alguns arquivos não foram coletados corretamente." -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "  - Arquivos não existem em static/" -ForegroundColor White
    Write-Host "  - STATICFILES_DIRS configurado incorretamente" -ForegroundColor White
    Write-Host "  - Permissões de arquivo" -ForegroundColor White
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host ""
