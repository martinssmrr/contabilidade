# 🐳 COMANDOS DOCKER - GESTÃO 360

Guia completo de comandos Docker para gerenciar o projeto Gestão 360 no Windows com PowerShell.

---

## 📋 ÍNDICE

- [Comandos Básicos](#comandos-básicos)
- [Gerenciamento de Containers](#gerenciamento-de-containers)
- [Gerenciamento de Imagens](#gerenciamento-de-imagens)
- [Logs e Monitoramento](#logs-e-monitoramento)
- [Comandos Django no Docker](#comandos-django-no-docker)
- [Banco de Dados](#banco-de-dados)
- [Limpeza e Manutenção](#limpeza-e-manutenção)
- [Troubleshooting](#troubleshooting)

---

## 🚀 COMANDOS BÁSICOS

### Iniciar o Projeto (Primeira Vez)
```powershell
# 1. Copiar arquivo de ambiente
Copy-Item .env.example .env

# 2. Editar o arquivo .env com suas credenciais
notepad .env

# 3. Construir as imagens e iniciar os containers
docker-compose up --build -d

# 4. Executar migrações
docker-compose exec web python manage.py migrate

# 5. Criar superusuário
docker-compose exec web python manage.py createsuperuser

# 6. Verificar status
docker-compose ps
```

### Iniciar o Projeto (Uso Diário)
```powershell
# Subir todos os serviços em background
docker-compose up -d

# Verificar se está rodando
docker-compose ps
```

### Parar o Projeto
```powershell
# Parar os containers (mantém dados)
docker-compose stop

# Parar e remover containers (mantém volumes)
docker-compose down

# Parar, remover containers E volumes (CUIDADO: apaga o banco!)
docker-compose down -v
```

### Reiniciar o Projeto
```powershell
# Reiniciar todos os serviços
docker-compose restart

# Reiniciar apenas um serviço específico
docker-compose restart web
docker-compose restart db
```

---

## 📦 GERENCIAMENTO DE CONTAINERS

### Listar Containers
```powershell
# Listar containers em execução
docker-compose ps

# Listar TODOS os containers (incluindo parados)
docker ps -a

# Listar apenas containers do projeto
docker-compose ps -a
```

### Ver Detalhes de um Container
```powershell
# Inspecionar container web
docker inspect gestao360_web

# Inspecionar container db
docker inspect gestao360_db

# Ver estatísticas de uso (CPU, memória, rede)
docker stats
```

### Acessar Terminal do Container
```powershell
# Acessar bash/shell do container web
docker-compose exec web bash

# Acessar bash/shell do container db
docker-compose exec db bash

# Acessar shell do PostgreSQL
docker-compose exec db psql -U postgres -d gestao360_db
```

### Executar Comandos Únicos
```powershell
# Executar comando no container web
docker-compose exec web ls -la

# Verificar versão do Python
docker-compose exec web python --version

# Verificar versão do Django
docker-compose exec web python manage.py --version
```

---

## 🖼️ GERENCIAMENTO DE IMAGENS

### Listar Imagens
```powershell
# Listar todas as imagens
docker images

# Listar imagens do projeto
docker images | Select-String "gestao360"
```

### Reconstruir Imagens
```powershell
# Reconstruir imagem do web (após mudanças no Dockerfile)
docker-compose build web

# Reconstruir TODAS as imagens
docker-compose build

# Forçar reconstrução sem cache
docker-compose build --no-cache

# Reconstruir e subir
docker-compose up --build -d
```

### Remover Imagens
```powershell
# Remover imagem específica
docker rmi gestao360_web

# Remover imagens não utilizadas
docker image prune

# Remover TODAS as imagens não utilizadas (CUIDADO!)
docker image prune -a
```

---

## 📊 LOGS E MONITORAMENTO

### Ver Logs
```powershell
# Ver logs de todos os serviços
docker-compose logs

# Ver logs em tempo real (follow)
docker-compose logs -f

# Ver logs apenas do web
docker-compose logs web

# Ver logs apenas do db
docker-compose logs db

# Ver logs em tempo real do web
docker-compose logs -f web

# Ver últimas 50 linhas
docker-compose logs --tail=50 web

# Ver logs com timestamp
docker-compose logs -t web
```

### Monitorar Recursos
```powershell
# Ver uso de CPU, memória, rede e I/O
docker stats

# Ver uso apenas dos containers do projeto
docker stats gestao360_web gestao360_db

# Ver processos rodando no container
docker-compose exec web ps aux
```

---

## 🐍 COMANDOS DJANGO NO DOCKER

### Migrações
```powershell
# Criar migrações
docker-compose exec web python manage.py makemigrations

# Aplicar migrações
docker-compose exec web python manage.py migrate

# Ver status das migrações
docker-compose exec web python manage.py showmigrations

# Reverter última migração
docker-compose exec web python manage.py migrate <app_name> <migration_name>
```

### Usuários e Admin
```powershell
# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Alterar senha de usuário
docker-compose exec web python manage.py changepassword <username>
```

### Shell e Testes
```powershell
# Abrir shell Python do Django
docker-compose exec web python manage.py shell

# Executar shell Python interativo (IPython se instalado)
docker-compose exec web python manage.py shell_plus

# Executar testes
docker-compose exec web python manage.py test

# Executar testes de um app específico
docker-compose exec web python manage.py test apps.users

# Executar testes com verbosidade
docker-compose exec web python manage.py test --verbosity=2
```

### Arquivos Estáticos
```powershell
# Coletar arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Limpar arquivos estáticos coletados
docker-compose exec web python manage.py collectstatic --clear --noinput
```

### Outros Comandos Django
```powershell
# Verificar problemas no projeto
docker-compose exec web python manage.py check

# Criar dados de teste (se tiver fixtures)
docker-compose exec web python manage.py loaddata <fixture_name>

# Exportar dados
docker-compose exec web python manage.py dumpdata > backup.json

# Executar servidor de desenvolvimento manualmente
docker-compose exec web python manage.py runserver 0.0.0.0:8000
```

---

## 🗄️ BANCO DE DADOS

### Acessar PostgreSQL
```powershell
# Acessar psql
docker-compose exec db psql -U postgres

# Acessar banco específico
docker-compose exec db psql -U postgres -d gestao360_db

# Listar bancos de dados
docker-compose exec db psql -U postgres -c "\l"

# Listar tabelas
docker-compose exec db psql -U postgres -d gestao360_db -c "\dt"
```

### Backup e Restore
```powershell
# Fazer backup do banco
docker-compose exec db pg_dump -U postgres gestao360_db > backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql

# Restaurar backup
Get-Content backup_20251113_143000.sql | docker-compose exec -T db psql -U postgres -d gestao360_db

# Backup em formato customizado (compactado)
docker-compose exec db pg_dump -U postgres -F c gestao360_db > backup.dump

# Restaurar dump customizado
docker-compose exec -T db pg_restore -U postgres -d gestao360_db < backup.dump
```

### Resetar Banco de Dados
```powershell
# CUIDADO: Isso apaga TODOS os dados!

# 1. Parar containers
docker-compose down

# 2. Remover volume do banco
docker volume rm gestao360_postgres_data

# 3. Subir novamente
docker-compose up -d

# 4. Executar migrações
docker-compose exec web python manage.py migrate

# 5. Criar superusuário
docker-compose exec web python manage.py createsuperuser
```

---

## 🧹 LIMPEZA E MANUTENÇÃO

### Limpar Recursos Não Utilizados
```powershell
# Remover containers parados
docker container prune

# Remover imagens não utilizadas
docker image prune

# Remover volumes não utilizados (CUIDADO!)
docker volume prune

# Remover redes não utilizadas
docker network prune

# Limpar TUDO (MUITO CUIDADO!)
docker system prune -a --volumes
```

### Ver Uso de Espaço
```powershell
# Ver espaço usado pelo Docker
docker system df

# Ver espaço detalhado
docker system df -v
```

### Remover Recursos Específicos do Projeto
```powershell
# Parar e remover containers
docker-compose down

# Remover imagens do projeto
docker rmi gestao360_web
docker rmi postgres:15-alpine

# Remover volumes (CUIDADO: apaga o banco!)
docker volume rm gestao360_postgres_data
docker volume rm gestao360_static_volume
docker volume rm gestao360_media_volume
```

---

## 🔧 TROUBLESHOOTING

### Container não Inicia
```powershell
# Ver logs de erro
docker-compose logs web
docker-compose logs db

# Verificar status
docker-compose ps

# Remover e recriar
docker-compose down
docker-compose up -d
```

### Erro de Conexão com Banco de Dados
```powershell
# Verificar se o banco está rodando
docker-compose ps db

# Ver logs do banco
docker-compose logs db

# Testar conexão manualmente
docker-compose exec db psql -U postgres -c "SELECT 1"

# Verificar variáveis de ambiente
docker-compose exec web env | Select-String "DB_"

# Reiniciar apenas o banco
docker-compose restart db
```

### Porta Já em Uso
```powershell
# Ver o que está usando a porta 8000
netstat -ano | Select-String ":8000"

# Matar processo na porta 8000 (substituir <PID>)
Stop-Process -Id <PID> -Force

# Ou mudar a porta no docker-compose.yml
# ports:
#   - "8001:8000"  # porta_host:porta_container
```

### Problemas com Volumes
```powershell
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect gestao360_postgres_data

# Remover volume específico (CUIDADO!)
docker-compose down
docker volume rm gestao360_postgres_data
docker-compose up -d
```

### Reconstruir Tudo do Zero
```powershell
# CUIDADO: Isso remove TUDO!

# 1. Parar e remover tudo
docker-compose down -v

# 2. Remover imagens
docker rmi $(docker images -q gestao360*)

# 3. Reconstruir
docker-compose build --no-cache

# 4. Subir
docker-compose up -d

# 5. Migrações e superusuário
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Erro "Cannot connect to Docker daemon"
```powershell
# Verificar se Docker Desktop está rodando
Get-Process "Docker Desktop" -ErrorAction SilentlyContinue

# Iniciar Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Aguardar e testar
Start-Sleep -Seconds 10
docker version
```

### Container Fica Reiniciando
```powershell
# Ver logs detalhados
docker-compose logs -f web

# Ver últimos 100 logs
docker-compose logs --tail=100 web

# Verificar código de saída
docker ps -a

# Acessar container mesmo que esteja falhando
docker run -it --entrypoint bash gestao360_web
```

---

## 📝 COMANDOS ÚTEIS COMBINADOS

### Reiniciar Desenvolvimento Completo
```powershell
# Reiniciar tudo e ver logs
docker-compose restart && docker-compose logs -f
```

### Atualizar Código e Dependências
```powershell
# Reconstruir após mudar requirements.txt ou Dockerfile
docker-compose down
docker-compose build --no-cache web
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Fazer Migrations Completas
```powershell
# Criar e aplicar migrações de todos os apps
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose restart web
```

### Backup Rápido antes de Mudanças
```powershell
# Backup do banco antes de alterações importantes
docker-compose exec db pg_dump -U postgres gestao360_db > backup_pre_update_$(Get-Date -Format "yyyyMMdd_HHmmss").sql
```

---

## 🎯 WORKFLOW RECOMENDADO

### Início do Dia
```powershell
# Subir projeto
docker-compose up -d

# Ver se está tudo ok
docker-compose ps

# Ver logs se necessário
docker-compose logs -f
```

### Durante Desenvolvimento
```powershell
# Após mudanças no código Python (hot reload automático)
# Nada precisa ser feito!

# Após mudanças em models.py
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Após mudanças em requirements.txt
docker-compose down
docker-compose build web
docker-compose up -d

# Após mudanças em Dockerfile
docker-compose down
docker-compose build --no-cache web
docker-compose up -d
```

### Fim do Dia
```powershell
# Parar containers (opcional, pode deixar rodando)
docker-compose stop

# Ou apenas deixar rodando em background
# (consome pouca memória quando idle)
```

---

## ⚠️ AVISOS IMPORTANTES

### ❌ NUNCA fazer isso:
```powershell
# NUNCA remover volumes sem backup em produção
docker-compose down -v  # Remove banco de dados!

# NUNCA fazer prune sem saber o que está fazendo
docker system prune -a --volumes  # Remove TUDO!
```

### ✅ SEMPRE fazer isso:
```powershell
# SEMPRE fazer backup antes de mudanças importantes
docker-compose exec db pg_dump -U postgres gestao360_db > backup.sql

# SEMPRE verificar logs em caso de erro
docker-compose logs web
docker-compose logs db

# SEMPRE testar em ambiente de desenvolvimento primeiro
```

---

## 🔗 LINKS ÚTEIS

- **Documentação Docker:** https://docs.docker.com/
- **Docker Compose:** https://docs.docker.com/compose/
- **PostgreSQL Docker:** https://hub.docker.com/_/postgres
- **Django com Docker:** https://docs.djangoproject.com/en/5.2/howto/deployment/

---

## 📞 AJUDA ADICIONAL

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs -f`
2. Verifique o status: `docker-compose ps`
3. Consulte a documentação oficial
4. Procure no Stack Overflow
5. Entre em contato com a equipe

---

**🐳 Docker configurado e pronto para uso! Happy coding!**
