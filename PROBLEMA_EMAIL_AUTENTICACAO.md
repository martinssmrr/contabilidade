# ⚠️ PROBLEMA IDENTIFICADO - Autenticação do E-mail

## 🔴 Erro Atual

```
SMTPAuthenticationError: (535, b'5.7.139 Authentication unsuccessful, 
basic authentication is disabled.')
```

## 📋 Causa

A Microsoft/Outlook **desabilitou** a autenticação básica (senha normal) para contas do Hotmail/Outlook por motivos de segurança.

## ✅ Soluções Disponíveis

### **Solução 1: Usar Senha de Aplicativo (Recomendado)**

1. **Acesse a conta Microsoft**:
   - Vá para: https://account.microsoft.com/security
   - Faça login com `contabilidadevetorial@hotmail.com`

2. **Ative a Verificação em Duas Etapas** (se ainda não estiver):
   - Clique em "Verificação em duas etapas"
   - Siga o processo de ativação

3. **Crie uma Senha de Aplicativo**:
   - Após ativar 2FA, volte para: https://account.microsoft.com/security
   - Clique em "Senhas de aplicativo" ou "App passwords"
   - Clique em "Criar nova senha de aplicativo"
   - Dê um nome: "Django Sistema Gestão 360"
   - **COPIE** a senha gerada (aparecerá apenas uma vez!)

4. **Atualize o arquivo `.env`**:
   ```env
   EMAIL_HOST_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Senha de aplicativo gerada
   ```

5. **Reinicie o container**:
   ```bash
   docker-compose restart web
   ```

---

### **Solução 2: Usar Gmail (Alternativa)**

Se não conseguir configurar o Hotmail, pode usar Gmail:

1. **Configure uma conta Gmail**
2. **Ative a Verificação em 2 Etapas**:
   - https://myaccount.google.com/security

3. **Crie uma Senha de Aplicativo**:
   - https://myaccount.google.com/apppasswords
   - Selecione "E-mail" e "Outro (nome personalizado)"
   - Nome: "Django Gestão 360"

4. **Atualize o `.env`**:
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=seu_email@gmail.com
   EMAIL_HOST_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Senha de aplicativo
   ```

5. **Reinicie o container**:
   ```bash
   docker-compose restart web
   ```

---

### **Solução 3: Usar SendGrid (Profissional)**

Para produção, é recomendado usar um serviço profissional:

1. **Crie conta no SendGrid** (gratuito até 100 e-mails/dia):
   - https://sendgrid.com/

2. **Gere uma API Key**

3. **Atualize o `.env`**:
   ```env
   EMAIL_HOST=smtp.sendgrid.net
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=SG.xxxxxx  # API Key do SendGrid
   ```

---

## 🧪 Como Testar Após Configurar

```bash
# 1. Reinicie o container
docker-compose restart web

# 2. Inicie o Celery worker
docker-compose exec -d web celery -A gestao360_project worker --loglevel=info

# 3. Teste envio direto
docker-compose exec web python manage.py shell
```

No shell Python:
```python
from django.core.mail import send_mail

resultado = send_mail(
    subject='Teste do Sistema',
    message='Este é um e-mail de teste',
    from_email='contabilidadevetorial@hotmail.com',
    recipient_list=['seu_email@teste.com'],
    fail_silently=False
)

print(f'E-mails enviados: {resultado}')
```

Se retornar `E-mails enviados: 1`, funcionou! ✅

---

## 🚀 Depois de Funcionar

1. **Teste o sistema completo**:
   - Acesse http://localhost:8000/admin/
   - Vá em "Documentos dos Clientes"
   - Adicione um novo documento
   - Cliente receberá e-mail automaticamente

2. **Monitore o Celery**:
   ```bash
   docker-compose exec web celery -A gestao360_project inspect active
   ```

3. **Verifique os logs**:
   ```bash
   docker-compose logs -f web | grep -i email
   ```

---

## 📧 Status Atual do Sistema

✅ Modelo `DocumentoCliente` - OK
✅ Celery configurado - OK  
✅ Redis funcionando - OK
✅ Tasks registradas - OK
✅ Admin customizado - OK
✅ Template HTML - OK
⚠️ **SMTP Autenticação** - **PENDENTE** (precisa senha de aplicativo)

---

## 🔐 Segurança

**IMPORTANTE:**
- ❌ **NÃO** commit a senha de aplicativo no repositório
- ✅ Mantenha apenas no arquivo `.env`
- ✅ O `.env` deve estar no `.gitignore`
- ✅ Use variáveis de ambiente em produção

---

## 📞 Suporte

Se tiver problemas:

1. Verifique se 2FA está ativo na conta Microsoft
2. Certifique-se de usar senha de **aplicativo**, não a senha normal
3. Teste conexão SMTP manualmente
4. Verifique firewall/antivírus não está bloqueando porta 587

**Após configurar a senha de aplicativo, o sistema estará 100% funcional!** 🎉
