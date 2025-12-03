# 📧 Guia de Uso - Sistema de Notificação de Documentos

## ✅ Sistema Instalado e Funcionando!

O sistema de notificação automática de documentos está **completamente funcional** e pronto para uso.

---

## 🎯 Como Funciona

1. **Staff faz upload** de um documento para um cliente no Django Admin
2. **Sistema salva** o documento no banco de dados automaticamente
3. **Signal dispara** uma task assíncrona do Celery
4. **E-mail é enviado** para o cliente notificando sobre o novo documento
5. **Cliente acessa** a área logada para visualizar/baixar o documento

> ⚠️ **LGPD Compliance**: O documento **NÃO é anexado** ao e-mail, apenas uma notificação é enviada.

---

## 🚀 Como Usar (Passo a Passo)

### 1️⃣ **Acesse o Django Admin**

```
http://localhost:8000/admin/
```

### 2️⃣ **Navegue até "Documentos dos Clientes"**

- No painel admin, procure por **"DOCUMENTS"**
- Clique em **"Documentos dos Clientes"**

### 3️⃣ **Adicione um Novo Documento**

Clique em **"Adicionar Documento do Cliente"** e preencha:

- **Cliente**: Selecione o cliente (apenas usuários não-staff aparecem)
- **Arquivo**: Faça upload do PDF, DOC, XLS, etc.
- **Tipo de Documento**: Escolha a categoria (Contrato Social, Certidão, etc.)
- **Título**: Nome descritivo (ex: "Contrato Social - Alteração 2025")
- **Descrição** *(opcional)*: Observações adicionais

### 4️⃣ **Salve o Documento**

Ao clicar em **"Salvar"**:

1. ✅ Documento é salvo no banco de dados
2. ✅ Signal automático dispara a task Celery
3. ✅ E-mail é enviado em background
4. ✅ Status "Notificação Enviada" fica verde ✓
5. ✅ Cliente recebe e-mail profissional com link

---

## 📊 Monitoramento

### **Ver Status dos Documentos**

Na lista de documentos no admin, você verá:

| Título | Cliente | Tipo | Status Notificação | Status Visualização |
|--------|---------|------|--------------------|---------------------|
| Contrato Social | João Silva | 📄 Contrato Social | ✅ Enviada | ⏳ Não visualizado |

- **✅ Enviada**: E-mail foi enviado com sucesso
- **⏳ Pendente**: E-mail ainda não foi enviado
- **👁️ Visualizado**: Cliente já viu o documento
- **⏳ Não visualizado**: Cliente ainda não abriu

### **Ver Logs de E-mail**

```bash
# No container Django
docker-compose exec web cat logs/email.log
```

### **Monitorar Celery (Flower)**

```bash
# Iniciar Flower (interface web)
docker-compose exec web celery -A vetorial_project flower --port=5555
```

Acesse: `http://localhost:5555`

---

## 🧪 Testar o Sistema

### **Teste Rápido**

```bash
# 1. Verifique se Redis está rodando
docker ps | grep redis

# 2. Verifique se Celery está ativo
docker-compose exec web celery -A vetorial_project inspect active

# 3. Envie um e-mail de teste
docker-compose exec web python manage.py shell
```

No shell Python:

```python
from apps.services.email_service import EmailService
from django.contrib.auth import get_user_model

User = get_user_model()

# Pegue um usuário cliente (não staff)
cliente = User.objects.filter(is_staff=False).first()

# Teste envio de e-mail
service = EmailService()
resultado = service.enviar_email_simples(
    destinatario=cliente.email,
    assunto="Teste de E-mail",
    corpo="Este é um e-mail de teste do sistema."
)

print(f"E-mail enviado: {resultado}")
```

---

## 📋 Requisitos Ativos

### **Containers Docker**

```bash
docker ps
```

Deve mostrar:
- ✅ `gestao360_web` (Django)
- ✅ `gestao360_db` (PostgreSQL)
- ✅ `gestao360_redis` (Redis)

### **Celery Worker**

```bash
# Verificar se está rodando
docker-compose exec web ps aux | grep celery
```

---

## 🔧 Comandos Úteis Docker

### **Ver Logs do Django**

```bash
docker-compose logs -f web
```

### **Ver Logs do Redis**

```bash
docker-compose logs -f redis
```

### **Reiniciar Celery Worker**

```bash
# Parar todos os workers
docker-compose exec web pkill -f celery

# Iniciar novo worker
docker-compose exec -d web celery -A vetorial_project worker --loglevel=info
```

### **Verificar Tasks na Fila**

```bash
docker-compose exec web celery -A vetorial_project inspect active
docker-compose exec web celery -A vetorial_project inspect scheduled
```

### **Limpar Fila Redis**

```bash
docker-compose exec redis redis-cli FLUSHALL
```

---

## 📧 Template do E-mail

O cliente receberá um e-mail com:

- ✅ Header com logo/nome da empresa
- ✅ Mensagem personalizada com nome do cliente
- ✅ Card do documento com tipo, título e data
- ✅ Descrição (se fornecida)
- ✅ Aviso LGPD (documento não anexado)
- ✅ Botão para acessar a área do cliente
- ✅ Link direto para login
- ✅ Rodapé com informações de contato

**Design:**
- 🎨 Profissional com gradient verde (#3ef47c → #2ed66b)
- 📱 Responsivo (funciona em mobile)
- 🔒 Seguro (sem anexos de documentos)

---

## ⚙️ Configurações (.env)

Certifique-se de que o arquivo `.env` contém:

```env
# E-mail Configuration
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=contabilidadevetorial@hotmail.com
EMAIL_HOST_PASSWORD=sua_senha_aqui

# Site URLs
SITE_URL=http://localhost:8000

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

## 🐛 Troubleshooting

### **E-mail não está sendo enviado**

1. Verifique se o Celery está rodando:
   ```bash
   docker-compose exec web celery -A vetorial_project inspect active
   ```

2. Verifique logs de e-mail:
   ```bash
   docker-compose exec web cat logs/email.log
   ```

3. Teste conexão SMTP:
   ```bash
   docker-compose exec web python manage.py shell
   ```
   ```python
   from django.core.mail import send_mail
   send_mail('Teste', 'Teste', 'contabilidadevetorial@hotmail.com', ['seu_email@teste.com'])
   ```

### **Redis não conecta**

```bash
# Verificar se está rodando
docker ps | grep redis

# Reiniciar Redis
docker-compose restart redis
```

### **Celery não processa tasks**

```bash
# Ver logs do Celery
docker-compose exec web celery -A vetorial_project inspect stats

# Reiniciar worker
docker-compose exec web pkill -f celery
docker-compose exec -d web celery -A vetorial_project worker --loglevel=info
```

---

## 📚 Documentação Adicional

Para mais detalhes técnicos, consulte:

- **DOCUMENTACAO_EMAILS.md**: Documentação técnica completa
- **GUIA_RAPIDO_EMAILS.md**: Guia de configuração e desenvolvimento
- **requirements.txt**: Dependências instaladas

---

## ✅ Checklist de Funcionamento

- [x] ✅ Modelo `DocumentoCliente` criado
- [x] ✅ Migrações aplicadas
- [x] ✅ Celery instalado e rodando
- [x] ✅ Redis ativo
- [x] ✅ Signal configurado
- [x] ✅ Template de e-mail criado
- [x] ✅ Admin customizado
- [x] ✅ Serviço de e-mail funcionando
- [x] ✅ Sistema pronto para uso!

---

## 🎉 Pronto!

O sistema está **100% funcional**. Basta:

1. Acessar o admin
2. Fazer upload de um documento
3. Cliente receberá e-mail automaticamente

**Suporte**: Se houver problemas, verifique os logs em `logs/email.log` ou use `docker-compose logs -f web`.
