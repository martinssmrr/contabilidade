# 🚀 Guia de Deploy - Vetorial

## Problema Identificado

Você está enfrentando dois problemas:

1. **CSS da calculadora não aparece** - Arquivos estáticos não foram coletados
2. **Logos novas (9-19.png) não aparecem** - Arquivos estáticos não foram coletados

## ✅ Solução Completa

### Opção 1: Script Automatizado (RECOMENDADO)

No servidor de produção, execute:

```bash
# Dar permissão de execução ao script
chmod +x deploy-production.sh

# Executar o deploy completo
./deploy-production.sh
```

O script faz tudo automaticamente:
- ✅ Git pull
- ✅ Rebuild do container
- ✅ Reinicia containers
- ✅ Aplica migrações
- ✅ **Coleta arquivos estáticos (resolve o problema!)**
- ✅ Ajusta permissões
- ✅ Reinicia o serviço web

---

### Opção 2: Comandos Manuais

Se preferir fazer passo a passo:

```bash
# 1. Baixar alterações
git pull origin master

# 2. Parar containers
docker-compose -f docker-compose.prod.yml down

# 3. Rebuild (apenas se houver mudanças no Dockerfile)
docker-compose -f docker-compose.prod.yml build --no-cache web

# 4. Subir containers
docker-compose -f docker-compose.prod.yml up -d

# 5. Aguardar 15 segundos
sleep 15

# 6. Aplicar migrações
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

# 7. IMPORTANTE: Coletar estáticos (resolve CSS + logos)
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput --clear

# 8. Ajustar permissões
docker-compose -f docker-compose.prod.yml exec web chmod -R 755 /app/staticfiles
docker-compose -f docker-compose.prod.yml exec web chmod -R 755 /app/media

# 9. Reiniciar serviço web
docker-compose -f docker-compose.prod.yml restart web
```

---

## 🔍 Verificar se Funcionou

### 1. Verificar logs
```bash
docker-compose -f docker-compose.prod.yml logs -f web
```

### 2. Verificar arquivos estáticos dentro do container
```bash
# Verificar CSS da calculadora
docker-compose -f docker-compose.prod.yml exec web ls -la /app/staticfiles/css/calculadora.css

# Verificar logos
docker-compose -f docker-compose.prod.yml exec web ls -la /app/staticfiles/img/
```

### 3. Testar no navegador
- Acesse: https://contabilvetorial.com.br/recursos/calculadora-clt-pj/
- Verifique se a calculadora está com o novo visual branco
- Scroll até a seção de logos de parceiros
- Verifique se todas as logos 1-19 estão aparecendo

### 4. Forçar refresh no navegador
- **Windows/Linux**: `Ctrl + Shift + R`
- **Mac**: `Cmd + Shift + R`

Isso garante que o navegador não use cache antigo.

---

## ⚠️ Por que Aconteceu?

O Django em produção não serve arquivos estáticos diretamente. Ele precisa:

1. **collectstatic**: Copiar todos os arquivos de `static/` para `staticfiles/`
2. **Nginx/Servidor Web**: Servir os arquivos de `staticfiles/`

Se você não rodar `collectstatic` após adicionar/modificar:
- Novos CSS
- Novas imagens
- Novos JS

Os arquivos não estarão disponíveis em produção.

---

## 📋 Checklist de Deploy

Sempre que fizer alterações em arquivos estáticos:

- [ ] Git add, commit, push
- [ ] SSH no servidor
- [ ] Git pull
- [ ] **Rodar collectstatic** ⚠️ (NUNCA ESQUECER!)
- [ ] Reiniciar serviço web
- [ ] Testar no navegador com hard refresh

---

## 🆘 Se Ainda Não Funcionar

### 1. Verificar se o volume está correto
```bash
docker volume ls | grep static
docker volume inspect vetorial_static_volume
```

### 2. Verificar configuração do settings.py
```python
# Deve ter:
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### 3. Verificar se o Nginx/servidor web está servindo corretamente
```bash
# Se estiver usando Nginx
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Limpar tudo e recomeçar
```bash
docker-compose -f docker-compose.prod.yml down -v  # Remove volumes
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput --clear
```

---

## 📞 Comandos Úteis

```bash
# Ver status dos containers
docker-compose -f docker-compose.prod.yml ps

# Ver logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f

# Entrar no container
docker-compose -f docker-compose.prod.yml exec web bash

# Reiniciar apenas o web (mais rápido)
docker-compose -f docker-compose.prod.yml restart web

# Ver uso de memória/CPU
docker stats
```

---

## ✨ Arquivos Afetados Neste Deploy

### Arquivos Estáticos
- `static/css/calculadora.css` - Nova versão (visual branco profissional)
- `static/img/1.png até 19.png` - Logos dos parceiros

### Templates
- `templates/recursos/calculadora_clt_pj.html` - Calculadora interativa
- `templates/trocar-contador.html` - Já tem logos 1-19

---

**Última atualização**: 3 de dezembro de 2025
