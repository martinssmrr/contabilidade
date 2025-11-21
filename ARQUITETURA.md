# 📐 ARQUITETURA COMPLETA - GESTÃO 360

## 🎯 VISÃO GERAL DO PROJETO

O **Gestão 360** é um sistema web de contabilidade online desenvolvido em Django que permite gerenciar clientes, serviços contábeis, pagamentos, documentos e suporte técnico.

---

## 📁 ESTRUTURA DE DIRETÓRIOS COMPLETA

```
gestao360/
│
├── apps/                              # Diretório contendo todos os apps do projeto
│   ├── __init__.py
│   │
│   ├── users/                         # App de Usuários e Autenticação
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py                   # Configuração do CustomUserAdmin
│   │   ├── apps.py
│   │   ├── models.py                  # Modelo CustomUser com campo 'role'
│   │   ├── tests.py
│   │   └── views.py
│   │
│   ├── dashboard/                     # App do Painel de Controle
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py                  # Sem modelos (usa outros apps)
│   │   ├── tests.py
│   │   ├── urls.py                    # URLs do dashboard
│   │   └── views.py                   # Views personalizadas por role
│   │
│   ├── services/                      # App de Serviços e Planos
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py                   # Admin para Service, Plan, Subscription
│   │   ├── apps.py
│   │   ├── models.py                  # Models: Service, Plan, Subscription
│   │   ├── tests.py
│   │   └── views.py
│   │
│   ├── payments/                      # App de Pagamentos
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py                   # Admin para Payment
│   │   ├── apps.py
│   │   ├── models.py                  # Model: Payment (integração Mercado Pago)
│   │   ├── tests.py
│   │   └── views.py                   # Lógica de processamento de pagamentos
│   │
│   ├── support/                       # App de Suporte (Tickets)
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py                   # Admin para Ticket, TicketMessage
│   │   ├── apps.py
│   │   ├── models.py                  # Models: Ticket, TicketMessage
│   │   ├── tests.py
│   │   └── views.py
│   │
│   └── documents/                     # App de Documentos
│       ├── migrations/
│       ├── __init__.py
│       ├── admin.py                   # Admin para Document
│       ├── apps.py
│       ├── models.py                  # Model: Document (upload de arquivos)
│       ├── tests.py
│       └── views.py
│
├── gestao360_project/                 # Configurações principais do Django
│   ├── __init__.py
│   ├── asgi.py                        # Configuração ASGI
│   ├── settings.py                    # Settings customizado com .env
│   ├── urls.py                        # URLs principais do projeto
│   └── wsgi.py                        # Configuração WSGI
│
├── static/                            # Arquivos estáticos globais
│   ├── css/
│   │   └── style.css                  # CSS customizado
│   ├── js/
│   │   └── script.js                  # JavaScript customizado
│   └── img/                           # Imagens do site
│
├── media/                             # Uploads de usuários
│   └── documents/                     # Documentos organizados por role/id
│
├── templates/                         # Templates HTML globais
│   ├── base.html                      # Template base
│   └── partials/
│       ├── navbar.html                # Navbar responsiva
│       └── footer.html                # Footer
│
├── .env.example                       # Exemplo de variáveis de ambiente
├── .gitignore                         # Arquivos ignorados pelo Git
├── Dockerfile                         # Configuração Docker
├── docker-compose.yml                 # Orquestração de containers
├── manage.py                          # Script de gerenciamento Django
├── README.md                          # Documentação principal
├── QUICKSTART.md                      # Guia de início rápido
└── requirements.txt                   # Dependências Python
```

---

## 🗄️ MODELOS DE DADOS (MODELS)

### 1. **users.CustomUser**
```python
- username (CharField)
- email (EmailField)
- first_name (CharField)
- last_name (CharField)
- role (CharField) → Choices: cliente, contador, admin, suporte
- telefone (CharField)
- cpf_cnpj (CharField)
- password (hashed)
- is_active, is_staff, is_superuser
```

**Responsabilidade:** Gerenciar usuários com diferentes níveis de acesso ao sistema.

---

### 2. **services.Service**
```python
- nome (CharField)
- descricao (TextField)
- preco (DecimalField)
- ativo (BooleanField)
- criado_em (DateTimeField)
- atualizado_em (DateTimeField)
```

**Responsabilidade:** Representar serviços avulsos (ex: Abertura de Empresa, Declaração IR).

---

### 3. **services.Plan**
```python
- nome (CharField)
- descricao (TextField)
- preco (DecimalField)
- periodo (CharField) → Choices: mensal, anual
- caracteristicas (TextField)
- ativo (BooleanField)
- criado_em (DateTimeField)
- atualizado_em (DateTimeField)
```

**Responsabilidade:** Representar planos de assinatura recorrentes.

---

### 4. **services.Subscription**
```python
- cliente (ForeignKey → CustomUser)
- plano (ForeignKey → Plan)
- status (CharField) → Choices: ativa, cancelada, suspensa, expirada
- data_inicio (DateField)
- data_fim (DateField)
- criado_em (DateTimeField)
- atualizado_em (DateTimeField)
```

**Responsabilidade:** Controlar assinaturas ativas dos clientes.

---

### 5. **payments.Payment**
```python
- cliente (ForeignKey → CustomUser)
- tipo (CharField) → Choices: servico, assinatura
- servico (ForeignKey → Service, nullable)
- plano (ForeignKey → Plan, nullable)
- valor (DecimalField)
- status (CharField) → Choices: pendente, aprovado, rejeitado, cancelado, reembolsado
- mp_payment_id (CharField)
- mp_preference_id (CharField)
- mp_status (CharField)
- criado_em (DateTimeField)
- atualizado_em (DateTimeField)
```

**Responsabilidade:** Processar e registrar pagamentos via Mercado Pago.

---

### 6. **support.Ticket**
```python
- titulo (CharField)
- descricao (TextField)
- cliente (ForeignKey → CustomUser)
- staff_designado (ForeignKey → CustomUser, nullable)
- status (CharField) → Choices: aberto, em_andamento, aguardando_cliente, concluido
- prioridade (CharField) → Choices: baixa, media, alta, urgente
- criado_em (DateTimeField)
- atualizado_em (DateTimeField)
```

**Responsabilidade:** Gerenciar tickets de suporte técnico.

---

### 7. **support.TicketMessage**
```python
- ticket (ForeignKey → Ticket)
- autor (ForeignKey → CustomUser)
- mensagem (TextField)
- criado_em (DateTimeField)
```

**Responsabilidade:** Armazenar mensagens/conversação de cada ticket.

---

### 8. **documents.Document**
```python
- titulo (CharField)
- descricao (TextField)
- arquivo (FileField)
- categoria (CharField) → Choices: relatorio, contrato, comprovante, declaracao, nota_fiscal, outros
- usuario (ForeignKey → CustomUser)
- visivel_para_cliente (BooleanField)
- criado_em (DateTimeField)
- atualizado_em (DateTimeField)
```

**Responsabilidade:** Gerenciar upload e armazenamento de documentos.

---

## ⚙️ ARQUIVOS DE CONFIGURAÇÃO

### **settings.py**
```python
✅ Carrega variáveis do .env usando python-dotenv
✅ Configuração do PostgreSQL
✅ AUTH_USER_MODEL = 'users.CustomUser'
✅ INSTALLED_APPS com todos os apps
✅ TEMPLATES com diretório templates/
✅ STATIC_URL, STATIC_ROOT, STATICFILES_DIRS
✅ MEDIA_URL, MEDIA_ROOT
✅ Configurações de segurança (SSL, CSRF, Cookies)
✅ Idioma: pt-br, Timezone: America/Sao_Paulo
✅ Variáveis do Mercado Pago
```

### **.env.example**
```env
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=

DB_NAME=gestao360_db
DB_USER=postgres
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432

MP_PUBLIC_KEY=
MP_ACCESS_TOKEN=
```

### **requirements.txt**
```
Django>=5.2,<6.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9.9
mercadopago>=2.2.0
django-environ>=0.11.2
Pillow>=10.0.0
```

### **Dockerfile**
```dockerfile
- Imagem base: Python 3.11-slim
- Instala dependências do PostgreSQL
- Copia requirements.txt e instala pacotes
- Copia código do projeto
- Expõe porta 8000
- Comando: runserver 0.0.0.0:8000
```

### **docker-compose.yml**
```yaml
Serviços:
  - db: PostgreSQL 15-alpine
  - web: Aplicação Django

Volumes:
  - postgres_data (persistência do banco)
  - static_volume (arquivos estáticos)
  - media_volume (uploads)

Portas:
  - 5432 (PostgreSQL)
  - 8000 (Django)
```

---

## 🎨 TEMPLATES E FRONTEND

### **base.html**
- Estrutura HTML5 responsiva
- Bootstrap 5
- Inclui navbar e footer
- Sistema de mensagens Django
- Blocos: title, extra_css, content, extra_js

### **navbar.html**
- Navegação condicional baseada em `user.is_authenticated`
- Links diferentes por `user.role`
- Dropdown de perfil

### **footer.html**
- Informações de contato
- Links rápidos
- Copyright

### **static/css/style.css**
- Estilos customizados
- Variáveis CSS
- Responsividade

### **static/js/script.js**
- Auto-dismiss de alertas
- Máscaras (CPF/CNPJ)
- Formatação de moeda
- Sistema de toasts

---

## 🔐 SEGURANÇA

### Implementações:
✅ AUTH_USER_MODEL customizado
✅ Passwords hasheadas (Django padrão)
✅ CSRF Protection
✅ XSS Protection
✅ Clickjacking Protection
✅ SSL/HTTPS (produção)
✅ Secure Cookies (produção)
✅ Variáveis de ambiente (.env)

---

## 🚀 FLUXO DE DESENVOLVIMENTO

### 1. **Ambiente de Desenvolvimento**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 2. **Ambiente Docker**
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 3. **Próximos Passos**
- [ ] Implementar views para cada app
- [ ] Criar templates específicos (dashboard/cliente.html, etc.)
- [ ] Configurar integração completa com Mercado Pago
- [ ] Adicionar sistema de autenticação (login/logout/registro)
- [ ] Implementar testes unitários
- [ ] Configurar CI/CD
- [ ] Deploy em servidor de produção

---

## 📊 DASHBOARDS POR ROLE

### **Cliente:**
- Visualizar assinaturas ativas
- Histórico de pagamentos
- Meus tickets de suporte
- Meus documentos

### **Contador:**
- Lista de clientes atribuídos
- Tickets abertos/em andamento
- Upload de documentos para clientes
- Relatórios

### **Admin:**
- Métricas gerais (receita, clientes, assinaturas)
- Gerenciar todos os usuários
- Aprovar/rejeitar pagamentos
- Acesso total ao Django Admin

### **Suporte:**
- Tickets atribuídos
- Responder tickets
- Alterar status de tickets
- Base de conhecimento

---

## 🔄 INTEGRAÇÕES

### **Mercado Pago:**
- Processar pagamentos de serviços avulsos
- Criar assinaturas recorrentes
- Webhooks para atualizar status de pagamentos
- Gerenciar reembolsos

---

## 📝 OBSERVAÇÕES IMPORTANTES

1. **Nunca** commitar o arquivo `.env` no repositório
2. Sempre usar `DEBUG=False` em produção
3. Configurar `ALLOWED_HOSTS` adequadamente
4. Usar HTTPS em produção
5. Fazer backup regular do banco de dados
6. Testar pagamentos no ambiente sandbox do Mercado Pago antes de ir para produção
7. Implementar logs para monitoramento
8. Configurar rate limiting para APIs

---

**🎉 Estrutura completa criada! O projeto está pronto para o desenvolvimento das funcionalidades!**
