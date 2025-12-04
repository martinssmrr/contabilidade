# 🚀 Guia Rápido de Deploy - Otimizações de Performance

## 📋 Checklist de Deploy

### 1. ✅ Código Commitado Localmente
```bash
git add .
git commit -m "feat: otimizações de performance - cache, compressão, preload"
git push origin master
```

### 2. 🔧 No Servidor (Via SSH)

#### 2.1 Executar Script de Deploy Automatizado
```bash
cd /root/vetorial
chmod +x deploy_optimized.sh
./deploy_optimized.sh
```

**OU executar manualmente:**

#### 2.2 Deploy Manual Passo a Passo

```bash
# Entrar no diretório
cd /root/vetorial

# Backup do banco
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres gestao360_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Puxar código
git pull origin master

# Instalar django-redis (se ainda não instalado)
docker-compose -f docker-compose.prod.yml exec web pip install django-redis

# Migrações
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Coletar estáticos
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput --clear

# Copiar estáticos para host
docker cp vetorial_web:/app/staticfiles/. /root/vetorial/staticfiles/

# Permissões
chmod -R 755 /root/vetorial/staticfiles/
chmod -R 755 /root/vetorial/media/

# Limpar cache
docker-compose -f docker-compose.prod.yml exec redis redis-cli FLUSHDB

# Reiniciar serviços
docker-compose -f docker-compose.prod.yml restart web celery_worker celery_beat

# Testar e recarregar Nginx
nginx -t && systemctl reload nginx
```

### 3. 🔍 Verificações Pós-Deploy

```bash
# Status dos containers
docker-compose -f docker-compose.prod.yml ps

# Logs do web
docker-compose -f docker-compose.prod.yml logs --tail=50 web

# Verificar cache Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli INFO stats

# Testar site
curl -I https://contabilvetorial.com.br
```

## 📊 Testes de Performance

### Online
1. **PageSpeed Insights**: https://pagespeed.web.dev/
2. **GTmetrix**: https://gtmetrix.com/
3. **WebPageTest**: https://www.webpagetest.org/

### Local
```bash
# Tempo de resposta
curl -o /dev/null -s -w "Time Total: %{time_total}s\n" https://contabilvetorial.com.br

# Headers de cache
curl -I https://contabilvetorial.com.br/static/css/style.css

# Compressão
curl -H "Accept-Encoding: gzip" -I https://contabilvetorial.com.br
```

## 🎯 Métricas Esperadas

### Antes das Otimizações
- ⚠️ Performance Score: ~63
- 🐌 First Contentful Paint: ~2.5s
- ⏱️ Time to Interactive: ~4.5s
- 📦 Total Size: ~3-4 MB

### Depois das Otimizações
- ✅ Performance Score: ~85-95
- ⚡ First Contentful Paint: ~1.0-1.5s
- 🚀 Time to Interactive: ~2.0-2.5s
- 📦 Total Size: ~1-1.5 MB (com compressão)

## 🔧 Configuração Nginx (Opcional - Melhoria Extra)

Se quiser aplicar a configuração otimizada do Nginx:

```bash
# Backup da configuração atual
cp /etc/nginx/sites-available/vetorial /etc/nginx/sites-available/vetorial.backup

# Copiar nova configuração (do arquivo nginx_optimized.conf)
# Editar conforme necessário
nano /etc/nginx/sites-available/vetorial

# Testar
nginx -t

# Se OK, recarregar
systemctl reload nginx
```

## 📝 Principais Mudanças Implementadas

### 1. ✨ Base.html
- ✅ Preconnect para CDNs
- ✅ DNS Prefetch
- ✅ CSS com preload (não bloqueia)
- ✅ JavaScript com defer

### 2. 🐍 Django Settings
- ✅ Cache Redis configurado
- ✅ Connection pooling do PostgreSQL
- ✅ Session cache
- ✅ Template caching
- ✅ WhiteNoise otimizado

### 3. 🔒 Middlewares
- ✅ Cache Control automático
- ✅ Security Headers
- ✅ Compressão habilitada

### 4. 🌐 Nginx (se aplicado)
- ✅ Gzip compression
- ✅ Cache de estáticos (1 ano)
- ✅ Cache de media (30 dias)
- ✅ Rate limiting
- ✅ Security headers

## ⚠️ Troubleshooting

### Cache não funciona
```bash
# Verificar Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli PING

# Testar cache no Django
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'ok', 30)
>>> cache.get('test')
```

### Estáticos não carregam
```bash
# Verificar arquivos
ls -la /root/vetorial/staticfiles/css/style.css

# Verificar permissões
stat /root/vetorial/staticfiles/

# Reexecutar collectstatic
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### Compressão não funciona
```bash
# Verificar módulos Nginx
nginx -V 2>&1 | grep gzip

# Testar compressão
curl -H "Accept-Encoding: gzip,deflate" -I https://contabilvetorial.com.br
```

## 📞 Suporte

Se encontrar problemas:
1. Verificar logs: `docker-compose -f docker-compose.prod.yml logs web`
2. Verificar status: `docker-compose -f docker-compose.prod.yml ps`
3. Rollback se necessário: `git checkout HEAD~1`

## 🎉 Resultado Final

Após o deploy, você deve ver:
- ⚡ Carregamento 40-50% mais rápido
- 📦 Tamanho reduzido em 60-70%
- 🚀 Menos queries ao banco (cache)
- 💾 Economia de bandwidth

**Teste agora mesmo**: https://contabilvetorial.com.br
