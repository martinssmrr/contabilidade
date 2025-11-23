# Vetorial - Sistema de Gestão Contábil

Sistema completo de gestão contábil desenvolvido em Django.

## 🚀 Deploy em Produção

Este projeto está preparado para deploy na VPS Hostinger com o domínio **contabilvetorial.com.br**.

### Pré-requisitos

- VPS Ubuntu 20.04/22.04
- Python 3.11+
- PostgreSQL 14+
- Nginx
- Domínio configurado

### Deploy Automático

Execute o script de deploy:

```bash
chmod +x deploy.sh
sudo ./deploy.sh
```

Para instruções detalhadas, consulte [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)

## 📋 Funcionalidades

- ✅ Sistema de autenticação e usuários
- ✅ Dashboard administrativo
- ✅ Gestão de serviços contábeis
- ✅ Sistema de pagamentos (Mercado Pago)
- ✅ Blog integrado
- ✅ Sistema de suporte/tickets
- ✅ Gestão de documentos
- ✅ Testemunhos de clientes
- ✅ Consulta de CNAEs
- ✅ Calculadora CLT vs PJ
- ✅ Wizard de abertura de empresa

## 🛠️ Tecnologias

- **Backend**: Django 5.2
- **Banco de Dados**: PostgreSQL
- **Frontend**: Bootstrap 5, JavaScript
- **Servidor Web**: Nginx + Gunicorn
- **SSL**: Let's Encrypt (Certbot)
- **Pagamentos**: Mercado Pago API

## 📦 Instalação Local

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/vetorial.git
cd vetorial
```

2. Crie ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale dependências
```bash
pip install -r requirements.txt
```

4. Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. Execute migrações
```bash
python manage.py migrate
```

6. Crie superusuário
```bash
python manage.py createsuperuser
```

7. Execute servidor de desenvolvimento
```bash
python manage.py runserver
```

## 🔧 Comandos Úteis

### Popular CNAEs
```bash
python manage.py popular_cnaes
```

### Coletar arquivos estáticos
```bash
python manage.py collectstatic
```

### Executar testes
```bash
python manage.py test
```

## 📁 Estrutura do Projeto

```
vetorial/
├── apps/
│   ├── blog/           # Sistema de blog
│   ├── dashboard/      # Dashboard administrativo
│   ├── documents/      # Gestão de documentos
│   ├── payments/       # Sistema de pagamentos
│   ├── services/       # Serviços contábeis
│   ├── support/        # Sistema de suporte
│   ├── testimonials/   # Testemunhos
│   └── users/          # Gestão de usuários
├── templates/          # Templates HTML
├── static/            # Arquivos estáticos
├── media/             # Uploads de usuários
├── vetorial_project/  # Configurações do projeto
├── deploy.sh          # Script de deploy automático
├── update.sh          # Script de atualização
├── backup.sh          # Script de backup
└── requirements.txt   # Dependências Python
```

## 🔐 Segurança

- ✅ HTTPS obrigatório em produção
- ✅ CSRF protection
- ✅ XSS protection
- ✅ Secure cookies
- ✅ SQL injection protection (ORM Django)
- ✅ Senhas hasheadas (PBKDF2)

## 📝 Variáveis de Ambiente

Configurar no arquivo `.env`:

```env
SECRET_KEY=sua-secret-key-segura
DEBUG=False
ALLOWED_HOSTS=contabilvetorial.com.br,www.contabilvetorial.com.br

DB_NAME=vetorial_db
DB_USER=vetorial_user
DB_PASSWORD=senha-segura
DB_HOST=localhost
DB_PORT=5432

MP_PUBLIC_KEY=sua-public-key
MP_ACCESS_TOKEN=seu-access-token
```

## 🚀 Atualização em Produção

Para atualizar o código em produção:

```bash
chmod +x update.sh
sudo ./update.sh
```

## 💾 Backup

Para fazer backup do banco de dados:

```bash
chmod +x backup.sh
sudo ./backup.sh
```

## 📞 Suporte

Para dúvidas e suporte, consulte:
- [Guia de Deploy](DEPLOY_GUIDE.md)
- [Documentação Django](https://docs.djangoproject.com/)
- [Hostinger Support](https://www.hostinger.com.br/suporte)

## 📄 Licença

Este projeto é proprietário e confidencial.

## 👥 Equipe

Desenvolvido por Vetorial Contabilidade

---

**Vetorial** - A Melhor Contabilidade Online Do Brasil
