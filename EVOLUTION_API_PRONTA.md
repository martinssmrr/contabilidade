# ✅ Evolution API Local - PRONTA PARA USAR!

## 🎉 Status: RODANDO!

Sua Evolution API está rodando localmente no Docker. Acesse:

**🌐 Evolution API Manager:** http://localhost:8080

### ✅ Instância Criada!
- **Nome:** `vetorial-local`
- **Status:** `close` (aguardando conexão com WhatsApp)
- **ID:** `32a7d394-0f65-4ef4-8596-35f34ccb9032`

**📱 PRÓXIMO PASSO:** Acesse http://localhost:8080 e escaneie o QR Code com seu WhatsApp!

⚠️ **IMPORTANTE:** Use comandos **PowerShell** (não bash/curl). Veja arquivo `COMANDOS_POWERSHELL.md` para referência completa.

---

## 📋 Informações para o `.env`

As configurações já estão no seu arquivo `.env`:

```env
EVOLUTION_API_URL=http://evolution-api:8080
EVOLUTION_API_KEY=B6D711FCDE4D4FD5936544120E713976
EVOLUTION_INSTANCE_NAME=vetorial-local
WHATSAPP_SENDER_NUMBER=5561998311920
```

✅ **Pronto! Não precisa alterar nada.**

---

## 📱 Como Conectar o WhatsApp (3 passos)

### 1. Criar Instância via PowerShell

**✅ JÁ CRIADA!** A instância `vetorial-local` já foi criada com sucesso.

Se precisar criar novamente:
```powershell
$body = @{
    instanceName = "vetorial-local"
    qrcode = $true
    integration = "WHATSAPP-BAILEYS"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/instance/create" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="B6D711FCDE4D4FD5936544120E713976"} -Body $body
```

### 2. Obter QR Code

**Via Interface Web (RECOMENDADO):**
Acesse: http://localhost:8080

**Via PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/connect/vetorial-local" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### 3. Escanear com WhatsApp

1. Abra WhatsApp no celular
2. **Configurações** > **Aparelhos conectados**
3. **Conectar aparelho**
4. Escaneie o QR Code

---

## 🧪 Testar Se Está Funcionando

### Teste Rápido via Django Shell

```powershell
docker-compose exec web python manage.py shell
```

Dentro do shell Python:

```python
from apps.support.whatsapp_service import whatsapp_service

# Verificar conexão
result = whatsapp_service.check_connection()
print(result)

# Enviar mensagem de teste (substitua pelo seu número)
result = whatsapp_service.send_welcome_message(
    phone='5561998311920',
    name='Teste Sistema'
)
print(result)
```

### Teste via Formulário (PowerShell)

```powershell
$lead = @{
    nome_completo = "João Teste"
    email = "joao@teste.com"
    telefone = "61998311920"
    estado = "DF"
    cidade = "Brasília"
    servico = "Teste WhatsApp"
    origem = "popup"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/support/capturar-lead/" -Method POST -Headers @{"Content-Type"="application/json"} -Body $lead
```

---

## 📊 Endpoints Úteis

### Ver Status da Conexão
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/connectionState/vetorial-local" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### Listar Instâncias
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/fetchInstances" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### Enviar Mensagem Direta (teste)
```powershell
$msg = @{
    number = "5561998311920"
    text = "Teste Evolution API Local!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/message/sendText/vetorial-local" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="B6D711FCDE4D4FD5936544120E713976"} -Body $msg
```

---

## 🔧 Comandos Docker Úteis

```bash
# Ver status dos containers
docker-compose ps

# Ver logs da Evolution API
docker-compose logs -f evolution-api

# Ver logs do Django
docker-compose logs -f web

# Reiniciar Evolution API
docker-compose restart evolution-api

# Parar tudo
docker-compose down

# Iniciar tudo
docker-compose up -d
```

---

## ⚠️ Importante

1. **API Key:** `B6D711FCDE4D4FD5936544120E713976` (já configurada)
2. **Instância:** `vetorial-local` (você vai criar via API)
3. **Porta:** `8080` (Evolution API) e `8000` (Django)
4. **Banco:** PostgreSQL compartilhado com Django

---

## 🎯 Próximo Passo

**Criar a instância WhatsApp** executando o comando do Passo 1 acima:

```bash
curl -X POST http://localhost:8080/instance/create \
  -H "Content-Type: application/json" \
  -H "apikey: B6D711FCDE4D4FD5936544120E713976" \
  -d '{
    "instanceName": "vetorial-local",
    "qrcode": true,
    "integration": "WHATSAPP-BAILEYS"
  }'
```

Depois obtenha o QR Code e escaneie com seu WhatsApp!

---

**Status:** ✅ Rodando em `http://localhost:8080`  
**Configuração:** ✅ Completa  
**Pronto para:** Conectar WhatsApp e enviar mensagens!
