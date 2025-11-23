# ==================================
# GUIA DE DEPLOY - VETORIAL
# VPS Hostinger - contabilvetorial.com.br
# ==================================

## REQUISITOS PRÉVIOS

1. VPS Hostinger com Ubuntu 20.04/22.04
2. Acesso SSH root ou sudo
3. Domínio contabilvetorial.com.br apontando para o IP da VPS
4. PostgreSQL será instalado durante o deploy

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
sudo ./deploy.sh
```

### 4. Configurar variáveis de ambiente

Edite o arquivo `.env` criado pelo script:

```bash
sudo nano /var/www/vetorial/.env
```

Configure:
- `SECRET_KEY`: Gere uma nova com o comando abaixo
- `DB_PASSWORD`: Senha segura do PostgreSQL
- `MP_PUBLIC_KEY` e `MP_ACCESS_TOKEN`: Credenciais do Mercado Pago

**Gerar SECRET_KEY:**
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Criar superusuário Django

```bash
cd /var/www/vetorial
sudo -u vetorial venv/bin/python manage.py createsuperuser
```

### 6. Popular dados iniciais (se necessário)

```bash
# Popular CNAEs
sudo -u vetorial venv/bin/python manage.py popular_cnaes

# Criar planos de exemplo (se tiver comando)
# sudo -u vetorial venv/bin/python manage.py criar_planos
```

## COMANDOS ÚTEIS

### Reiniciar aplicação
```bash
sudo systemctl restart gunicorn-vetorial
```

### Ver logs da aplicação
```bash
sudo journalctl -u gunicorn-vetorial -f
```

### Ver logs do Nginx
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Coletar arquivos estáticos
```bash
cd /var/www/vetorial
sudo -u vetorial venv/bin/python manage.py collectstatic --noinput
```

### Executar migrações
```bash
cd /var/www/vetorial
sudo -u vetorial venv/bin/python manage.py migrate
```

### Acessar shell Django
```bash
cd /var/www/vetorial
sudo -u vetorial venv/bin/python manage.py shell
```

### Backup do banco de dados
```bash
sudo -u postgres pg_dump vetorial_db > backup_$(date +%Y%m%d).sql
```

### Restaurar banco de dados
```bash
sudo -u postgres psql vetorial_db < backup_20250123.sql
```

## CONFIGURAÇÃO DNS

Configure os seguintes registros no painel do seu domínio:

```
Tipo    Nome    Valor               TTL
A       @       SEU_IP_DA_VPS       3600
A       www     SEU_IP_DA_VPS       3600
```

## MONITORAMENTO

### Verificar status dos serviços
```bash
sudo systemctl status gunicorn-vetorial
sudo systemctl status nginx
sudo systemctl status postgresql
```

### Verificar uso de recursos
```bash
htop
df -h
free -h
```

## SEGURANÇA

### Firewall (UFW)
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Atualizar sistema regularmente
```bash
sudo apt update && sudo apt upgrade -y
```

### Renovação SSL automática
O Certbot já está configurado para renovar automaticamente.
Para testar:
```bash
sudo certbot renew --dry-run
```

## TROUBLESHOOTING

### Erro 502 Bad Gateway
```bash
# Verificar se Gunicorn está rodando
sudo systemctl status gunicorn-vetorial

# Verificar logs
sudo journalctl -u gunicorn-vetorial -n 50

# Reiniciar serviço
sudo systemctl restart gunicorn-vetorial
```

### Erro 500 Internal Server Error
```bash
# Verificar logs da aplicação
sudo journalctl -u gunicorn-vetorial -n 100

# Verificar DEBUG está False
sudo nano /var/www/vetorial/vetorial_project/settings.py

# Coletar static files novamente
cd /var/www/vetorial
sudo -u vetorial venv/bin/python manage.py collectstatic --noinput
```

### CSS/JS não carregando
```bash
# Coletar arquivos estáticos
cd /var/www/vetorial
sudo -u vetorial venv/bin/python manage.py collectstatic --noinput

# Verificar permissões
sudo chown -R vetorial:www-data /var/www/vetorial/staticfiles
sudo chmod -R 755 /var/www/vetorial/staticfiles
```

### Banco de dados não conecta
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Testar conexão
sudo -u postgres psql -d vetorial_db -U vetorial_user

# Verificar configurações no .env
sudo nano /var/www/vetorial/.env
```

## MANUTENÇÃO

### Atualizar código
```bash
cd /var/www/vetorial
sudo -u vetorial git pull origin main
sudo -u vetorial venv/bin/pip install -r requirements.txt
sudo -u vetorial venv/bin/python manage.py migrate
sudo -u vetorial venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart gunicorn-vetorial
```

### Logs de acesso
```bash
# Limpar logs antigos (cuidado!)
sudo journalctl --vacuum-time=7d
```

## CONTATOS DE SUPORTE

- Hostinger: https://www.hostinger.com.br/suporte
- Django: https://docs.djangoproject.com/
- Nginx: https://nginx.org/en/docs/

## CHECKLIST PÓS-DEPLOY

- [ ] Site acessível via HTTPS
- [ ] Admin Django funcionando (/admin/)
- [ ] CSS e imagens carregando corretamente
- [ ] Formulários de contato funcionando
- [ ] Cadastro de usuários funcionando
- [ ] Sistema de pagamento configurado
- [ ] Backup do banco de dados agendado
- [ ] Monitoramento configurado
- [ ] SSL renovação automática ativa
- [ ] Firewall configurado
- [ ] DNS propagado corretamente
