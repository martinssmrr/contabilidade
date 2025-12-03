# 🔧 Configurar Gmail para Envio de E-mails - Guia Rápido

## ⚡ Problema Atual

A conta `contabilidadevetorial@hotmail.com` não pode ser usada porque:
- ❌ Autenticação básica está desabilitada pela Microsoft
- ❌ Conta não tem verificação em 2 etapas configurada (necessária para senha de aplicativo)

## ✅ Solução: Usar Gmail (5 minutos)

### **Passo 1: Ativar Verificação em 2 Etapas**

1. Acesse: https://myaccount.google.com/security
2. Faça login com sua conta Gmail (`martinssmrr@gmail.com`)
3. Procure por **"Verificação em duas etapas"**
4. Clique em **"Ativar"**
5. Siga o processo (geralmente pede número de telefone)

### **Passo 2: Criar Senha de Aplicativo**

1. Após ativar 2FA, acesse: https://myaccount.google.com/apppasswords
2. Se não ver a opção:
   - Volte para https://myaccount.google.com/security
   - Role até encontrar "Senhas de app" ou "App passwords"
3. Clique em **"Selecionar app"** → Escolha **"E-mail"**
4. Clique em **"Selecionar dispositivo"** → Escolha **"Outro (nome personalizado)"**
5. Digite: **"Django Gestão 360"**
6. Clique em **"Gerar"**
7. **COPIE A SENHA DE 16 CARACTERES** (formato: xxxx xxxx xxxx xxxx)
   - ⚠️ Aparecerá apenas uma vez!

### **Passo 3: Atualizar o `.env`**

Abra o arquivo `.env` e cole a senha (SEM espaços):

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=martinssmrr@gmail.com
EMAIL_HOST_PASSWORD=xxxxxxxxxxxxxxxx  # Cole a senha de 16 dígitos SEM espaços
```

### **Passo 4: Reiniciar o Sistema**

```bash
# No terminal
docker-compose restart web
```

### **Passo 5: Testar**

```bash
docker-compose exec web python manage.py shell
```

No shell Python:
```python
from django.core.mail import send_mail

resultado = send_mail(
    'Teste Sistema',
    'Teste de configuração',
    'martinssmrr@gmail.com',
    ['martinssmrr@gmail.com'],
    fail_silently=False
)

print(f'Enviado: {resultado}')
```

Se mostrar `Enviado: 1` → **SUCESSO!** ✅

---

## 🔄 Alternativa: Corrigir o Hotmail

Se preferir usar o Hotmail, siga estes passos:

### **1. Ativar Verificação em 2 Etapas no Hotmail**

1. Acesse: https://account.microsoft.com/security
2. Login com `contabilidadevetorial@hotmail.com`
3. Procure **"Verificação em duas etapas"** ou **"Two-step verification"**
4. Clique em **"Ativar"** e siga o processo

### **2. Criar Senha de Aplicativo**

1. Após ativar 2FA, na mesma página de segurança:
2. Procure por **"Senhas de aplicativo"** ou **"App passwords"**
3. Clique em **"Criar nova senha de aplicativo"**
4. Digite nome: **"Django Sistema"**
5. **COPIE** a senha gerada
6. Cole no `.env`:

```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=contabilidadevetorial@hotmail.com
EMAIL_HOST_PASSWORD=xxxxxxxxxxxx  # Senha de aplicativo (SEM traços)
```

---

## 🎯 Recomendação

**Use Gmail** - É mais rápido e fácil de configurar, e funciona perfeitamente para o sistema.

Depois que o e-mail estiver funcionando, você pode:
- Mudar o `from_email` nos templates para aparecer como "Vetorial Contabilidade"
- Configurar DKIM/SPF para melhorar entregabilidade
- Usar um serviço profissional (SendGrid, Mailgun) em produção

---

## ⏱️ Tempo Estimado

- Gmail: **5 minutos**
- Hotmail (se 2FA já estiver ativo): **3 minutos**
- Hotmail (sem 2FA): **10 minutos**

---

## 📞 Após Configurar

Execute:
```bash
docker-compose restart web
docker-compose exec -d web celery -A gestao360_project worker --loglevel=info
```

E teste enviando um documento no admin! 🚀
