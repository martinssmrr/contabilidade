# 🚨 FIX URGENTE - Arquivos Estáticos Não Aparecem

## Problema Identificado

**Causa Raiz**: O arquivo `gestao360_project/settings.py` estava com:
```python
STATIC_URL = "static/"  # ❌ ERRADO - sem barra inicial
```

Deveria ser:
```python
STATIC_URL = "/static/"  # ✅ CORRETO - com barra inicial
```

Isso fazia o Django procurar arquivos em URLs erradas, causando:
- ❌ CSS da calculadora não carrega
- ❌ Logos 9-19.png não aparecem
- ❌ Outros arquivos estáticos não funcionam

## ✅ Correções Aplicadas

1. **STATIC_URL** corrigido para `/static/`
2. **STORAGES** adicionado com WhiteNoise configurado
3. **ALLOWED_HOSTS** e **CSRF_TRUSTED_ORIGINS** configurados
4. Script de deploy melhorado para limpar e recoletar estáticos

---

## 📋 COMANDOS PARA EXECUTAR NO SERVIDOR

Execute os comandos abaixo **NESTA ORDEM** no servidor de produção:

### 1️⃣ Acessar diretório do projeto
```bash
cd /caminho/para/vetorial
```

### 2️⃣ Puxar alterações do Git
```bash
git pull origin master
```

### 3️⃣ Dar permissão ao script de deploy
```bash
chmod +x deploy-production.sh
```

### 4️⃣ Executar deploy automatizado
```bash
./deploy-production.sh
```

O script vai:
- ✅ Parar containers
- ✅ Rebuild do container web
- ✅ Subir containers
- ✅ Aplicar migrações
- ✅ **LIMPAR staticfiles completamente**
- ✅ **Coletar novos arquivos estáticos**
- ✅ Ajustar permissões
- ✅ Reiniciar serviço web

---

## 🔍 Verificação Manual (se o script não funcionar)

Se o script automatizado falhar, execute manualmente:

```bash
# 1. Pull do Git
git pull origin master

# 2. Parar tudo
docker-compose -f docker-compose.prod.yml down

# 3. Rebuild do web
docker-compose -f docker-compose.prod.yml build --no-cache web

# 4. Subir containers
docker-compose -f docker-compose.prod.yml up -d

# 5. Aguardar 20 segundos
sleep 20

# 6. LIMPAR staticfiles
docker-compose -f docker-compose.prod.yml exec web rm -rf /app/staticfiles/*
docker-compose -f docker-compose.prod.yml exec web mkdir -p /app/staticfiles

# 7. Coletar estáticos NOVOS
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# 8. Verificar se CSS foi coletado
docker-compose -f docker-compose.prod.yml exec web ls -lh /app/staticfiles/css/calculadora.css

# 9. Verificar se logos foram coletadas
docker-compose -f docker-compose.prod.yml exec web ls /app/staticfiles/img/ | grep -E "^[0-9]+\.png$"

# 10. Ajustar permissões
docker-compose -f docker-compose.prod.yml exec web chmod -R 755 /app/staticfiles

# 11. Reiniciar web
docker-compose -f docker-compose.prod.yml restart web
```

---

## ✅ Como Verificar se Funcionou

### No Terminal do Servidor:

```bash
# 1. Verificar CSS da calculadora
docker-compose -f docker-compose.prod.yml exec web cat /app/staticfiles/css/calculadora.css | head -20

# Deve mostrar o conteúdo do CSS (começando com comentários e regras CSS)
```

```bash
# 2. Verificar logos
docker-compose -f docker-compose.prod.yml exec web ls -la /app/staticfiles/img/ | grep "\.png$"

# Deve listar 1.png até 19.png
```

### No Navegador:

1. **Acessar a calculadora**:
   - URL: https://contabilvetorial.com.br/recursos/calculadora-clt-pj/
   - Deve aparecer calculadora com fundo branco, botões cinza claros
   - Display deve estar visível e estilizado

2. **Verificar logos**:
   - Scroll até a seção "Empresas que confiam"
   - Deve mostrar 19 logos rolando em loop contínuo

3. **Forçar refresh sem cache**:
   - **Windows/Linux**: `Ctrl + Shift + R`
   - **Mac**: `Cmd + Shift + R`

---

## 🆘 Se AINDA Não Funcionar

### Diagnóstico Avançado:

```bash
# 1. Ver configuração do Django
docker-compose -f docker-compose.prod.yml exec web python manage.py diffsettings | grep STATIC

# Deve mostrar:
# STATIC_ROOT = '/app/staticfiles'
# STATIC_URL = '/static/'
# STATICFILES_DIRS = ['/app/static']
```

```bash
# 2. Verificar se o volume está correto
docker volume inspect vetorial_static_volume

# 3. Ver logs do web
docker-compose -f docker-compose.prod.yml logs web | tail -100

# 4. Testar URL diretamente
docker-compose -f docker-compose.prod.yml exec web curl http://localhost:8000/static/css/calculadora.css -I

# Deve retornar HTTP 200
```

### Se o Nginx estiver envolvido:

```bash
# Verificar configuração do Nginx
sudo cat /etc/nginx/sites-available/contabilvetorial.com.br | grep static

# Deve ter algo como:
# location /static/ {
#     alias /caminho/para/staticfiles/;
# }

# Reiniciar Nginx
sudo systemctl restart nginx
sudo nginx -t  # Testar configuração
```

---

## 📁 Arquivos Modificados

### Commitados no Git:

1. **gestao360_project/settings.py**
   - ✅ `STATIC_URL = "/static/"` (corrigido)
   - ✅ `STORAGES` adicionado (WhiteNoise)
   - ✅ `ALLOWED_HOSTS` configurado
   - ✅ `CSRF_TRUSTED_ORIGINS` configurado

2. **deploy-production.sh**
   - ✅ Melhorado com limpeza de staticfiles
   - ✅ Verificações adicionadas

3. **static/css/calculadora.css**
   - ✅ Visual branco profissional (13.389 bytes)

4. **static/img/**
   - ✅ Logos 1.png até 19.png presentes

---

## 💡 Por Que Aconteceu?

O Django usa `STATIC_URL` para construir as URLs dos arquivos estáticos nos templates.

**Sem a barra inicial `/`:**
```html
<!-- Template gera: -->
<link href="static/css/calculadora.css">

<!-- Navegador procura em: -->
https://contabilvetorial.com.br/recursos/static/css/calculadora.css  ❌ ERRADO
```

**Com a barra inicial `/`:**
```html
<!-- Template gera: -->
<link href="/static/css/calculadora.css">

<!-- Navegador procura em: -->
https://contabilvetorial.com.br/static/css/calculadora.css  ✅ CORRETO
```

---

## 📞 Checklist Final

Após executar o deploy, marque:

- [ ] Script `./deploy-production.sh` executado sem erros
- [ ] Arquivo `/app/staticfiles/css/calculadora.css` existe (verificado via `docker exec`)
- [ ] Arquivos `/app/staticfiles/img/1.png` até `19.png` existem
- [ ] Site carrega sem erro 404 no console do navegador (F12)
- [ ] Calculadora aparece com visual branco e botões estilizados
- [ ] Logos 1-19 aparecem na seção de parceiros
- [ ] Hard refresh feito no navegador (`Ctrl+Shift+R`)

---

## 🎯 Resultado Esperado

**Antes do Fix:**
- ❌ Calculadora sem estilo (HTML puro)
- ❌ Logos 9-19 não aparecem
- ❌ Console mostra erros 404 para CSS

**Depois do Fix:**
- ✅ Calculadora com fundo branco profissional
- ✅ Botões cinza claro com efeito 3D
- ✅ Display branco com texto escuro
- ✅ Todas 19 logos aparecem rolando
- ✅ Nenhum erro 404 no console

---

**Última atualização**: 3 de dezembro de 2025 - 23:45  
**Commit**: `d395f93` - fix: corrige STATIC_URL com barra inicial e adiciona WhiteNoise STORAGES
