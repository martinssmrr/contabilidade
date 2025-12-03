# 📧 Sistema de Notificação Automática de Documentos

## 🎯 Visão Geral

Sistema completo de envio automático de e-mails para notificação de documentos enviados pela equipe interna (staff) aos clientes.

**Características principais:**
- ✅ Upload de documentos pelo Django Admin
- ✅ Notificação automática por e-mail via Celery
- ✅ Template HTML profissional
- ✅ Conformidade com LGPD (documentos não são anexados)
- ✅ Tracking de visualização e notificação
- ✅ Testes unitários completos

---

## 📂 Arquitetura do Sistema

```
vetorial_project/
├── apps/
│   ├── documents/
│   │   ├── models_documento_cliente.py   # Modelo DocumentoCliente
│   │   ├── models.py                     # Import do modelo
│   │   ├── admin.py                      # Admin customizado
│   │   ├── signals.py                    # Signal post_save
│   │   ├── tasks.py                      # Tasks do Celery
│   │   ├── apps.py                       # Config + registro signals
│   │   └── tests/
│   │       └── test_documento_cliente.py # Testes completos
│   └── services/
│       └── email_service.py              # Serviço de e-mail
├── templates/
│   └── emails/
│       └── notificacao_documento.html    # Template do e-mail
└── vetorial_project/
    ├── celery.py                         # Configuração Celery
    ├── settings.py                       # Settings atualizados
    └── __init__.py                       # Import Celery
```

---

## 🔧 Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install celery redis django-redis
```

### 2. Instalar e Iniciar Redis

**Windows:**
```bash
# Baixar Redis: https://github.com/microsoftarchive/redis/releases
# Ou usar Docker:
docker run -d -p 6379:6379 redis:alpine
```

**Linux/Mac:**
```bash
sudo apt-get install redis-server
redis-server
```

### 3. Configurar Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha:

```env
EMAIL_HOST_USER=contabilidadevetorial@hotmail.com
EMAIL_HOST_PASSWORD=sua-senha-aqui
CELERY_BROKER_URL=redis://localhost:6379/0
SITE_URL=http://localhost:8000
```

### 4. Aplicar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar Superusuário (se necessário)

```bash
python manage.py createsuperuser
```

---

## 🚀 Como Executar

### 1. Iniciar Django

```bash
python manage.py runserver
```

### 2. Iniciar Celery Worker (em outro terminal)

```bash
celery -A vetorial_project worker -l info
```

**Windows:**
```bash
celery -A vetorial_project worker -l info --pool=solo
```

### 3. (Opcional) Monitorar Tasks com Flower

```bash
pip install flower
celery -A vetorial_project flower
# Acesse: http://localhost:5555
```

---

## 📋 Como Usar

### 1. Acessar Django Admin

```
http://localhost:8000/admin/
```

### 2. Navegar para "Documentos dos Clientes"

```
/admin/documents/documentocliente/
```

### 3. Adicionar Novo Documento

1. Clique em "Adicionar Documento do Cliente"
2. Selecione o **Cliente** (usuário com email)
3. Escolha o **Tipo de Documento**
4. Preencha **Título** e **Descrição** (opcional)
5. Faça **Upload do Arquivo**
6. Clique em "Salvar"

### 4. O que acontece automaticamente:

```
1. Documento é salvo no banco de dados
   ↓
2. Signal post_save é disparado
   ↓
3. Task do Celery é agendada
   ↓
4. E-mail é enviado em background
   ↓
5. Status atualizado: notificacao_enviada = True
```

---

## 📧 E-mail Enviado

**Assunto:**
```
📄 Novo documento disponível - [Tipo do Documento]
```

**Conteúdo:**
- Saudação personalizada com nome do cliente
- Informações do documento (tipo, título, descrição)
- Data de envio
- Botão de ação para acessar área do cliente
- Aviso de segurança (LGPD)
- Rodapé com contatos

**Conformidade LGPD:**
- ✅ Documento NÃO é anexado ao e-mail
- ✅ Cliente acessa via login na área segura
- ✅ Link direto para documentos

---

## 🧪 Executar Testes

### Rodar todos os testes:

```bash
python manage.py test apps.documents.tests
```

### Rodar teste específico:

```bash
python manage.py test apps.documents.tests.test_documento_cliente.DocumentoClienteModelTest
```

### Com pytest:

```bash
pip install pytest pytest-django
pytest apps/documents/tests/
```

### Cobertura de testes:

```bash
pip install coverage
coverage run --source='apps.documents,apps.services' manage.py test
coverage report
coverage html
```

---

## 🔍 Monitoramento e Logs

### Logs são salvos em:

```
logs/
├── django.log      # Logs gerais
└── emails.log      # Logs específicos de e-mail
```

### Ver logs em tempo real:

**Linux/Mac:**
```bash
tail -f logs/emails.log
```

**Windows:**
```bash
Get-Content logs\emails.log -Wait
```

---

## 🛠️ Troubleshooting

### ❌ E-mail não está sendo enviado

1. **Verificar Celery Worker está rodando:**
   ```bash
   celery -A vetorial_project inspect active
   ```

2. **Verificar Redis está ativo:**
   ```bash
   redis-cli ping
   # Deve retornar: PONG
   ```

3. **Verificar configurações de e-mail:**
   ```python
   python manage.py shell
   >>> from django.core.mail import send_mail
   >>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
   ```

4. **Verificar logs:**
   ```bash
   cat logs/emails.log
   ```

### ❌ Erro "ModuleNotFoundError: No module named 'celery'"

```bash
pip install celery redis
```

### ❌ Cliente não recebe e-mail

1. Verificar se cliente tem email cadastrado
2. Verificar spam/lixo eletrônico
3. Verificar senha do Hotmail está correta no .env
4. Verificar se Hotmail permite "aplicativos menos seguros"

---

## 📊 Modelo de Dados

### DocumentoCliente

| Campo                | Tipo           | Descrição                                    |
|----------------------|----------------|----------------------------------------------|
| cliente              | ForeignKey     | Usuário (cliente) que recebe                 |
| arquivo              | FileField      | Arquivo do documento                         |
| tipo_documento       | CharField      | Categoria (contrato, certidão, etc)          |
| titulo               | CharField      | Título descritivo                            |
| descricao            | TextField      | Descrição adicional (opcional)               |
| enviado_por          | ForeignKey     | Staff que fez upload                         |
| data_envio           | DateTimeField  | Data/hora do envio (auto)                    |
| visualizado          | BooleanField   | Se cliente visualizou                        |
| data_visualizacao    | DateTimeField  | Data/hora da visualização                    |
| notificacao_enviada  | BooleanField   | Se e-mail foi enviado                        |
| data_notificacao     | DateTimeField  | Data/hora do envio do e-mail                 |

---

## 🔐 Segurança e LGPD

### Conformidade Implementada:

1. **Não anexar documentos em e-mail:**
   - `EMAIL_ATTACH_DOCUMENTS = False` (settings)
   - Apenas notificação é enviada

2. **Acesso via login:**
   - Cliente precisa autenticar para ver documento
   - Link seguro para área do cliente

3. **Retenção de logs:**
   - Logs mantidos por 90 dias (configurável)
   - `NOTIFICATION_LOG_RETENTION_DAYS = 90`

4. **Criptografia:**
   - Conexão SMTP usa TLS
   - `EMAIL_USE_TLS = True`

---

## 📚 Referências e Documentação

- **Django Signals:** https://docs.djangoproject.com/en/5.2/topics/signals/
- **Celery:** https://docs.celeryproject.org/
- **Django Email:** https://docs.djangoproject.com/en/5.2/topics/email/
- **Redis:** https://redis.io/documentation

---

## 🤝 Suporte

Para dúvidas ou problemas:

📧 **E-mail:** contabilidadevetorial@hotmail.com  
🌐 **Site:** www.contabilvetorial.com.br

---

## 📝 Licença

© 2025 Contabilidade Vetorial. Todos os direitos reservados.

---

**Desenvolvido com ❤️ pela equipe Vetorial**
