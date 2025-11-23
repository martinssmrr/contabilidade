# ✅ CHECKLIST DE DEPLOY - VETORIAL
# contabilvetorial.com.br

## ANTES DO DEPLOY

### Configurações do Projeto
- [ ] Arquivo `.env` configurado com valores de produção
- [ ] `DEBUG=False` no arquivo `.env`
- [ ] `SECRET_KEY` gerada de forma segura
- [ ] `ALLOWED_HOSTS` configurado com domínio correto
- [ ] Dependências atualizadas em `requirements.txt`
- [ ] Migrações do banco de dados criadas e testadas
- [ ] Arquivos estáticos coletados localmente para teste

### Credenciais e Acessos
- [ ] Credenciais do Mercado Pago (Public Key e Access Token)
- [ ] Senha do PostgreSQL definida
- [ ] Acesso SSH à VPS Hostinger
- [ ] Domínio contabilvetorial.com.br apontando para IP da VPS

### DNS e Domínio
- [ ] Registro A para @ apontando para IP da VPS
- [ ] Registro A para www apontando para IP da VPS
- [ ] Propagação DNS verificada (pode levar até 24h)

## DURANTE O DEPLOY

### Preparação do Servidor
- [ ] Conectado via SSH à VPS
- [ ] Sistema atualizado (`apt update && apt upgrade`)
- [ ] Python 3.11 instalado
- [ ] PostgreSQL instalado
- [ ] Nginx instalado
- [ ] Git instalado (se usar repositório)

### Upload e Configuração
- [ ] Projeto enviado para `/var/www/vetorial`
- [ ] Script `deploy.sh` com permissão de execução
- [ ] Script executado com sucesso
- [ ] Arquivo `.env` configurado no servidor
- [ ] Banco de dados PostgreSQL criado
- [ ] Usuário do banco criado com permissões

### Aplicação Django
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Migrações executadas (`python manage.py migrate`)
- [ ] Superusuário criado (`python manage.py createsuperuser`)
- [ ] CNAEs populados (`python manage.py popular_cnaes`)
- [ ] Arquivos estáticos coletados (`python manage.py collectstatic`)

### Gunicorn e Nginx
- [ ] Gunicorn socket criado
- [ ] Gunicorn service criado
- [ ] Gunicorn iniciado e habilitado
- [ ] Configuração Nginx criada em `/etc/nginx/sites-available/`
- [ ] Link simbólico criado em `/etc/nginx/sites-enabled/`
- [ ] Configuração Nginx testada (`nginx -t`)
- [ ] Nginx reiniciado

### SSL/HTTPS
- [ ] Certbot instalado
- [ ] Certificado SSL gerado para domínio principal
- [ ] Certificado SSL gerado para www
- [ ] Renovação automática configurada
- [ ] Teste de renovação executado (`certbot renew --dry-run`)

### Firewall e Segurança
- [ ] UFW instalado
- [ ] Portas 22, 80, 443 abertas
- [ ] UFW habilitado
- [ ] Permissões de arquivo configuradas corretamente

## APÓS O DEPLOY

### Testes Básicos
- [ ] Site acessível via HTTP (http://contabilvetorial.com.br)
- [ ] Redirecionamento automático para HTTPS funcionando
- [ ] Site acessível via HTTPS (https://contabilvetorial.com.br)
- [ ] www redirecionando corretamente
- [ ] Página inicial carregando
- [ ] CSS e JavaScript carregando
- [ ] Imagens aparecendo

### Funcionalidades do Site
- [ ] Navegação entre páginas funcionando
- [ ] Página de Planos carregando
- [ ] Toggle entre Serviços e Comércio funcionando
- [ ] Página de Consulta CNAEs funcionando
- [ ] Calculadora CLT vs PJ funcionando
- [ ] FAQ expandindo/colapsando
- [ ] Formulários de contato funcionando

### Admin Django
- [ ] Admin acessível (/admin/)
- [ ] Login no admin funcionando
- [ ] CSS do admin carregando
- [ ] Modelos aparecendo no admin
- [ ] CRUD de planos funcionando
- [ ] Upload de imagens funcionando

### Sistema de Pagamentos
- [ ] Credenciais do Mercado Pago configuradas
- [ ] Processo de abertura de empresa iniciando
- [ ] Wizard de etapas funcionando
- [ ] Integração com Mercado Pago testada (modo sandbox primeiro)

### Performance e Logs
- [ ] Gunicorn rodando sem erros (`systemctl status gunicorn-vetorial`)
- [ ] Nginx sem erros nos logs (`tail -f /var/log/nginx/error.log`)
- [ ] Aplicação sem erros (`journalctl -u gunicorn-vetorial -f`)
- [ ] Tempo de carregamento aceitável (< 3s)
- [ ] Imagens otimizadas

### Backup e Manutenção
- [ ] Script de backup criado e testado
- [ ] Primeiro backup manual executado
- [ ] Cron job para backup automático configurado (opcional)
- [ ] Documentação de comandos úteis salva

### SEO e Marketing
- [ ] Título e meta descrições configurados
- [ ] Favicon funcionando
- [ ] Google Analytics instalado (se aplicável)
- [ ] Sitemap.xml gerado (opcional)
- [ ] robots.txt configurado (opcional)

### Monitoramento
- [ ] Logs sendo gerados corretamente
- [ ] Espaço em disco verificado (`df -h`)
- [ ] Memória verificada (`free -h`)
- [ ] Processos rodando corretamente (`htop`)

## TESTES FINAIS

### Navegação Completa
- [ ] Home page
- [ ] Página de Planos
- [ ] Página de Serviços
- [ ] Consulta CNAEs
- [ ] Calculadora CLT vs PJ
- [ ] Blog (se ativo)
- [ ] Página de contato
- [ ] Admin Django

### Dispositivos
- [ ] Desktop (Chrome)
- [ ] Desktop (Firefox)
- [ ] Mobile (Chrome)
- [ ] Mobile (Safari)
- [ ] Tablet

### Performance
- [ ] Google PageSpeed Insights > 80
- [ ] GTmetrix Grade > B
- [ ] Tempo de resposta < 2s

## DOCUMENTAÇÃO

- [ ] Credenciais salvas em local seguro
- [ ] IPs e acessos documentados
- [ ] Comandos úteis salvos
- [ ] Contatos de suporte anotados
- [ ] README atualizado

## PÓS-DEPLOY (7 DIAS)

- [ ] Monitorar logs diariamente
- [ ] Verificar uso de recursos
- [ ] Testar backup e restauração
- [ ] Coletar feedback de usuários
- [ ] Ajustar performance se necessário
- [ ] Configurar monitoramento automático (Sentry, UptimeRobot, etc)

## COMANDOS DE EMERGÊNCIA

```bash
# Reiniciar aplicação
sudo systemctl restart gunicorn-vetorial

# Ver logs em tempo real
sudo journalctl -u gunicorn-vetorial -f

# Reiniciar Nginx
sudo systemctl restart nginx

# Restaurar backup
sudo -u postgres psql vetorial_db < backup.sql

# Coletar static files
cd /var/www/vetorial
sudo -u vetorial venv/bin/python manage.py collectstatic --noinput

# Verificar status geral
sudo systemctl status gunicorn-vetorial
sudo systemctl status nginx
sudo systemctl status postgresql
```

## CONTATOS IMPORTANTES

- **Hostinger Suporte**: https://www.hostinger.com.br/suporte
- **Django Docs**: https://docs.djangoproject.com/
- **Mercado Pago Devs**: https://www.mercadopago.com.br/developers/

---

**Data do Deploy**: _________________
**Responsável**: _________________
**Versão**: 1.0.0
