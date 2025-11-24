# 🚀 GUIA DE ATUALIZAÇÃO - PULL SIMPLES (DOCKER)

## Passos para atualizar o site após fazer push no GitHub:

### 1. Conectar na VPS via SSH
```bash
ssh seu_usuario@seu_servidor_ip
```

### 2. Navegar até o diretório do projeto
```bash
cd /home/seu_usuario/vetorial
```

### 3. Fazer pull das alterações
```bash
git pull origin master
```

### 4. Rebuild e restart dos containers
```bash
docker-compose down
docker-compose up -d --build
```

### 5. Coletar arquivos estáticos dentro do container
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### 6. Executar migrações (se houver alterações no banco)
```bash
docker-compose exec web python manage.py migrate
```

### 7. Verificar status dos containers
```bash
docker-compose ps
```

### 8. Ver logs (se necessário)
```bash
docker-compose logs -f web
```

---

## 📝 COMANDO RÁPIDO (TUDO DE UMA VEZ):

```bash
cd /home/seu_usuario/vetorial && \
git pull origin master && \
docker-compose down && \
docker-compose up -d --build && \
docker-compose exec web python manage.py collectstatic --noinput && \
docker-compose exec web python manage.py migrate && \
echo "✅ Deploy concluído!" && \
docker-compose ps
```

---

## 🔄 ALTERNATIVA RÁPIDA (SEM REBUILD - se não houver mudanças no Dockerfile):

```bash
cd /home/seu_usuario/vetorial && \
git pull origin master && \
docker-compose restart web && \
docker-compose exec web python manage.py collectstatic --noinput && \
echo "✅ Atualização rápida concluída!"
```

---

## ⚠️ PONTOS DE ATENÇÃO DESTA ATUALIZAÇÃO:

### Alterações realizadas:
- ✅ Imagens de background agora são configuráveis por página (hero sections)
- ✅ CTA Section transformada em card com bordas arredondadas
- ✅ Modal popup com botão X visível
- ✅ Modal popup configurado para abrir em 3 segundos
- ✅ Página `/abrir-empresa/` criada com modal integrado
- ✅ Página `/services/planos/` corrigida (background hero adicionado)
- ✅ Configurações de produção atualizadas (ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS)

### Arquivos modificados principais:
- `templates/home.html` - Hero section com background inline
- `templates/abrir_empresa.html` - Nova página criada
- `templates/services/planos.html` - Background hero corrigido
- `static/css/style.css` - Botão close do modal, hero section
- `gestao360_project/urls.py` - Nova rota `/abrir-empresa/`
- `vetorial_project/settings.py` - Domínio adicionado

### Nenhuma migração de banco necessária
- ✅ Não houve alterações em models

---

## 🔍 VERIFICAÇÕES PÓS-DEPLOY:

1. Testar abertura do site: https://contabilvetorial.com.br
2. Verificar se o modal popup abre após 3 segundos
3. Testar página: https://contabilvetorial.com.br/abrir-empresa/
4. Verificar se imagens de hero sections carregam corretamente
5. Testar botões "Abra sua empresa agora" (devem abrir modal)
6. Verificar se o card CTA tem bordas arredondadas
7. Testar botão X do modal (deve estar visível e funcional)

---

## 🆘 TROUBLESHOOTING:

### ❌ ERRO 502 Bad Gateway:
```bash
# 1. Verificar se os containers estão rodando
docker-compose ps

# 2. Ver logs do container web
docker-compose logs web

# 3. Se o container não estiver rodando, subir novamente
docker-compose up -d

# 4. Se o container estiver crashando, ver erro completo
docker-compose logs --tail=50 web

# 5. Verificar se o banco está acessível
docker-compose exec web python manage.py check --deploy

# 6. Restart completo se necessário
docker-compose down && docker-compose up -d --build
```

### Ver logs do container web:
```bash
docker-compose logs -f web
```

### Ver logs de todos os containers:
```bash
docker-compose logs -f
```

### Se o container não subir:
```bash
docker-compose ps
docker-compose logs web
```

### Se arquivos estáticos não carregarem:
```bash
docker-compose exec web python manage.py collectstatic --noinput --clear
docker-compose restart web
```

### Entrar no container para debug:
```bash
docker-compose exec web bash
```

### Rebuild forçado (limpa cache):
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Verificar containers rodando:
```bash
docker ps
```

### Verificar uso de recursos:
```bash
docker stats
```







docker-compose down && \
docker-compose up -d --build && \
docker-compose exec web python manage.py collectstatic --noinput && \
docker-compose exec web python manage.py migrate && \
docker-compose ps