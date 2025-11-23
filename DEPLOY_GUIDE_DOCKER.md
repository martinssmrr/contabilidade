# ==================================
# GUIA DE DEPLOY DOCKER - VETORIAL
# VPS Hostinger - contabilvetorial.com.br
# ==================================

## ARQUITETURA

O projeto usa Docker Compose com os seguintes containers:
- **nginx**: Servidor web (portas 80/443)
- **web**: Django + Gunicorn (porta 8000)
- **db**: PostgreSQL 15 (porta 5432)
- **certbot**: Gerenciamento SSL (Let's Encrypt)

## REQUISITOS PRÉVIOS

1. VPS Hostinger com Ubuntu 20.04/22.04
2. Acesso SSH root ou sudo
3. Domínio contabilvetorial.com.br apontando para o IP da VPS
4. Pelo menos 2GB RAM e 20GB de disco

## PASSOS PARA DEPLOY

### 1. Conectar na VPS via SSH

```bash
ssh root@seu-ip-da-vps
```

### 2. Fazer upload do projeto

**Opção A - Via Git (Recomendado):**
```bash
cd /var/www
git clone https://github.com/seu-usuario/vetorial.git
cd vetorial
```

**Opção B - Via SCP/SFTP:**
```bash
# Do seu computador local:
scp -r C:\Users\teste\OneDrive\Desktop\vetorial root@seu-ip-da-vps:/var/www/
```

### 3. Executar o script de deploy

```bash
cd /var/www/vetorial
chmod +x deploy.sh
./deploy.sh
```

O script irá:
- Instalar Docker e Docker Compose
- Criar arquivo .env
- Construir imagens Docker
- Iniciar containers
- Executar migrações
- Configurar SSL

### 4. Editar variáveis de ambiente

Durante o deploy, você será solicitado a editar o `.env`:

```bash
nano /var/www/vetorial/.env
```

Configure:
```env
SECRET_KEY=gere_uma_chave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=contabilvetorial.com.br,www.contabilvetorial.com.br

DB_NAME=vetorial_db
DB_USER=vetorial_user
DB_PASSWORD=senha_segura_do_postgresql
DB_HOST=db
DB_PORT=5432

MP_PUBLIC_KEY=sua-public-key-mercadopago
MP_ACCESS_TOKEN=seu-access-token-mercadopago
```

**Gerar SECRET_KEY:**
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## COMANDOS ÚTEIS DOCKER

### Gerenciamento de Containers

```bash
cd /var/www/vetorial

# Ver status dos containers
docker-compose -f docker-compose.prod.yml ps

# Ver logs de todos os containers
docker-compose -f docker-compose.prod.yml logs -f

# Ver logs apenas do web (Django)
docker-compose -f docker-compose.prod.yml logs -f web

# Ver logs apenas do nginx
docker-compose -f docker-compose.prod.yml logs -f nginx

# Ver logs do banco
docker-compose -f docker-compose.prod.yml logs -f db

# Reiniciar containers
docker-compose -f docker-compose.prod.yml restart

# Reiniciar apenas um container
docker-compose -f docker-compose.prod.yml restart web

# Parar containers
docker-compose -f docker-compose.prod.yml down

# Iniciar containers
docker-compose -f docker-compose.prod.yml up -d

# Rebuild e restart
docker-compose -f docker-compose.prod.yml up -d --build
```

### Comandos Django no Container

```bash
# Acessar shell Django
docker-compose -f docker-compose.prod.yml exec web python manage.py shell

# Executar migrações
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Criar migrações
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations

# Coletar arquivos estáticos
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Criar superusuário
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Popular CNAEs
docker-compose -f docker-compose.prod.yml exec web python manage.py popular_cnaes

# Acessar bash do container
docker-compose -f docker-compose.prod.yml exec web bash
```

### Banco de Dados

```bash
# Acessar PostgreSQL
docker-compose -f docker-compose.prod.yml exec db psql -U vetorial_user -d vetorial_db

# Fazer backup manual
./backup-docker.sh

# Restaurar backup
gunzip -c backups/backup_20250123_120000.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T db \
  psql -U vetorial_user -d vetorial_db
```

### Atualização de Código

```bash
# Script automático de atualização
chmod +x update-docker.sh
./update-docker.sh

# Ou manual:
git pull origin main
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## CONFIGURAÇÃO DNS

Configure os seguintes registros no painel do seu domínio:

```
Tipo    Nome    Valor               TTL
A       @       SEU_IP_DA_VPS       3600
A       www     SEU_IP_DA_VPS       3600
```

## MONITORAMENTO

### Verificar recursos do sistema

```bash
# Uso de disco pelos containers
docker system df

# Ver uso de recursos em tempo real
docker stats

# Espaço em disco
df -h

# Memória
free -h
```

### Ver containers rodando

```bash
docker ps
```

### Limpar recursos não utilizados

```bash
# Remover containers parados
docker container prune

# Remover imagens não utilizadas
docker image prune

# Remover tudo não utilizado (CUIDADO!)
docker system prune -a
```

## SEGURANÇA

### Firewall (UFW)

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Renovação SSL

A renovação é automática via cron job. Para testar:

```bash
docker-compose -f docker-compose.prod.yml run --rm certbot renew --dry-run
```

Para renovar manualmente:

```bash
docker-compose -f docker-compose.prod.yml run --rm certbot renew
docker-compose -f docker-compose.prod.yml restart nginx
```

## TROUBLESHOOTING

### Erro 502 Bad Gateway

```bash
# Verificar se web está rodando
docker-compose -f docker-compose.prod.yml ps

# Ver logs do web
docker-compose -f docker-compose.prod.yml logs web

# Reiniciar web
docker-compose -f docker-compose.prod.yml restart web
```

### Erro 500 Internal Server Error

```bash
# Ver logs detalhados
docker-compose -f docker-compose.prod.yml logs -f web

# Verificar se DEBUG está False
cat .env | grep DEBUG

# Coletar static files novamente
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### CSS/JS não carregando

```bash
# Verificar nginx está servindo static
docker-compose -f docker-compose.prod.yml logs nginx

# Coletar arquivos estáticos
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Reiniciar nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### Banco de dados não conecta

```bash
# Verificar se db está rodando
docker-compose -f docker-compose.prod.yml ps db

# Ver logs do banco
docker-compose -f docker-compose.prod.yml logs db

# Testar conexão
docker-compose -f docker-compose.prod.yml exec db psql -U vetorial_user -d vetorial_db

# Reiniciar banco (CUIDADO!)
docker-compose -f docker-compose.prod.yml restart db
```

### Container não inicia

```bash
# Ver motivo do erro
docker-compose -f docker-compose.prod.yml logs nome-do-container

# Rebuild do container
docker-compose -f docker-compose.prod.yml build nome-do-container
docker-compose -f docker-compose.prod.yml up -d
```

## BACKUP E RESTAURAÇÃO

### Backup automático

O backup é executado automaticamente às 2h da manhã via cron.

### Backup manual

```bash
./backup-docker.sh
```

### Restaurar backup

```bash
# Listar backups disponíveis
ls -lh backups/

# Restaurar backup específico
gunzip -c backups/backup_20250123_120000.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T db \
  psql -U vetorial_user -d vetorial_db
```

## VOLUMES DOCKER

Os volumes persistem dados mesmo quando containers são removidos:

```bash
# Listar volumes
docker volume ls

# Ver detalhes de um volume
docker volume inspect vetorial_postgres_data

# Backup de volume (avançado)
docker run --rm -v vetorial_postgres_data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/postgres_backup.tar.gz /data
```

## PERFORMANCE

### Otimizar imagens Docker

```bash
# Remover imagens antigas
docker image prune -a

# Rebuild otimizado
docker-compose -f docker-compose.prod.yml build --no-cache
```

### Escalar workers Gunicorn

Edite `docker-compose.prod.yml` e ajuste `--workers`:

```yaml
command: gunicorn vetorial_project.wsgi:application --bind 0.0.0.0:8000 --workers 5
```

Depois:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## LOGS

### Rotação de logs Docker

Edite `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Reinicie Docker:
```bash
sudo systemctl restart docker
```

## CHECKLIST PÓS-DEPLOY

- [ ] Todos os containers rodando (`docker-compose ps`)
- [ ] Site acessível via HTTPS
- [ ] Admin Django funcionando
- [ ] CSS e JS carregando
- [ ] Formulários funcionando
- [ ] Backup automático configurado
- [ ] SSL renovação automática ativa
- [ ] Firewall configurado
- [ ] DNS propagado
- [ ] Logs sendo gerados
- [ ] Monitoramento ativo

## CONTATOS DE SUPORTE

- Hostinger: https://www.hostinger.com.br/suporte
- Django: https://docs.djangoproject.com/
- Docker: https://docs.docker.com/

---

**Vetorial** - Deploy com Docker
