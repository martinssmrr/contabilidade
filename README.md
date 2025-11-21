# 🏢 Gestão 360 - Sistema de Contabilidade Online

Sistema web completo de contabilidade online desenvolvido em Django, com integração ao Mercado Pago, gerenciamento de usuários, serviços, documentos e sistema de tickets.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Apps do Sistema](#apps-do-sistema)
- [Uso com Docker](#uso-com-docker)
- [Comandos Úteis](#comandos-úteis)

## 🎯 Sobre o Projeto

O **Gestão 360** é uma plataforma completa de contabilidade online que permite:
- Gestão de clientes e contadores
- Venda de serviços avulsos e planos de assinatura
- Processamento de pagamentos via Mercado Pago
- Sistema de tickets para suporte
- Gerenciamento de documentos e relatórios
- Dashboards personalizados por tipo de usuário

## 🚀 Tecnologias Utilizadas

- **Framework:** Django 5.2+
- **Banco de Dados:** PostgreSQL
- **Pagamentos:** Mercado Pago API
- **Containerização:** Docker & Docker Compose
- **Frontend:** Bootstrap 5, JavaScript
- **Segurança:** SSL/TLS, Django Security Features

## 📁 Estrutura do Projeto

```
gestao360/
├── apps/
│   ├── users/          # Gerenciamento de usuários e autenticação
│   ├── dashboard/      # Painéis personalizados por role
│   ├── services/       # Serviços e planos de assinatura
│   ├── payments/       # Processamento de pagamentos
│   ├── support/        # Sistema de tickets
│   └── documents/      # Gerenciamento de arquivos
├── gestao360_project/  # Configurações do projeto Django
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── media/              # Uploads de usuários
├── templates/          # Templates HTML globais
├── .env.example        # Exemplo de variáveis de ambiente
├── requirements.txt    # Dependências Python
├── Dockerfile          # Configuração Docker
├── docker-compose.yml  # Orquestração de containers
└── manage.py           # Gerenciador Django
```

## 🔧 Instalação

### Pré-requisitos

- Python 3.11+
- PostgreSQL 15+
- Docker e Docker Compose (opcional)

### Instalação Local

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/gestao360.git
cd gestao360
```

2. **Crie e ative um ambiente virtual:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

5. **Execute as migrações:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crie um superusuário:**
```bash
python manage.py createsuperuser
```

7. **Inicie o servidor:**
```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```env
# Django
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=gestao360_db
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

# Mercado Pago
MP_PUBLIC_KEY=sua_public_key
MP_ACCESS_TOKEN=seu_access_token
```

### Gerar SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📦 Apps do Sistema

### 1. **Users** (Usuários)
- Modelo: `CustomUser` com campo `role`
- Roles disponíveis: cliente, contador, admin, suporte
- Gerenciamento de perfis e permissões

### 2. **Dashboard** (Painel)
- Views personalizadas por tipo de usuário
- Estatísticas e métricas
- Acesso rápido a funcionalidades

### 3. **Services** (Serviços)
- **Service**: Serviços avulsos (ex: Abertura de Empresa)
- **Plan**: Planos de assinatura (mensal/anual)
- **Subscription**: Controle de assinaturas ativas

### 4. **Payments** (Pagamentos)
- Integração com Mercado Pago
- Processamento de pagamentos
- Histórico de transações

### 5. **Support** (Suporte)
- **Ticket**: Sistema de tickets
- **TicketMessage**: Mensagens/conversação
- Status: Aberto, Em Andamento, Aguardando Cliente, Concluído

### 6. **Documents** (Documentos)
- Upload de arquivos (PDFs, contratos, relatórios)
- Organização por categoria
- Controle de visibilidade

## 🐳 Uso com Docker

### Iniciar todos os serviços:
```bash
docker-compose up -d
```

### Executar migrações:
```bash
docker-compose exec web python manage.py migrate
```

### Criar superusuário:
```bash
docker-compose exec web python manage.py createsuperuser
```

### Ver logs:
```bash
docker-compose logs -f
```

### Parar os serviços:
```bash
docker-compose down
```

## 📝 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar shell interativo
python manage.py shell

# Executar testes
python manage.py test
```

## 🔒 Segurança

Em **produção**, certifique-se de:
- ✅ Definir `DEBUG=False`
- ✅ Usar uma `SECRET_KEY` forte e única
- ✅ Configurar `ALLOWED_HOSTS` corretamente
- ✅ Habilitar HTTPS/SSL
- ✅ Usar variáveis de ambiente para credenciais
- ✅ Configurar CORS e CSRF adequadamente

## 📄 Licença

Este projeto está sob a licença MIT.

## 👥 Autores

**Gestão 360 Team**

## 📞 Contato

- Email: contato@gestao360.com.br
- WhatsApp: (11) 91234-5678

---

**Gestão 360** - Sua contabilidade online simplificada! 🚀
