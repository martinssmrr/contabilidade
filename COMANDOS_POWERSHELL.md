# 🚀 Comandos PowerShell - Evolution API

## ✅ Instância Criada!

A instância `vetorial-local` foi criada com sucesso!

**Status:** `close` (aguardando conexão com WhatsApp)

---

## 📱 Como Conectar o WhatsApp

### Opção 1: Via Interface Web (RECOMENDADO)

Acesse no navegador:
```
http://localhost:8080
```

1. Você verá a instância `vetorial-local` listada
2. Clique no botão de **"Connect"** ou **QR Code**
3. Escaneie o QR Code com seu WhatsApp

### Opção 2: Via PowerShell

**Obter QR Code em base64:**
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8080/instance/connect/vetorial-local" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
$response | ConvertTo-Json
```

**Verificar status da conexão:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/connectionState/vetorial-local" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

---

## 📊 Comandos Úteis (PowerShell)

### Listar Todas as Instâncias
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/fetchInstances" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### Ver Detalhes da Instância
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/fetchInstances?instanceName=vetorial-local" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### Verificar Status da Conexão
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/connectionState/vetorial-local" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

Quando conectado, deve retornar:
```
instance        state
--------        -----
vetorial-local  open
```

### Enviar Mensagem de Teste
```powershell
$mensagem = @{
    number = "5561998311920"
    text = "Olá! Esta é uma mensagem de teste da Evolution API local."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/message/sendText/vetorial-local" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="B6D711FCDE4D4FD5936544120E713976"} -Body $mensagem
```

### Desconectar Instância
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/logout/vetorial-local" -Method DELETE -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### Deletar Instância
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/delete/vetorial-local" -Method DELETE -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

---

## 🧪 Testar Integração Django

### Via Python Shell
```powershell
docker-compose exec web python manage.py shell
```

Dentro do shell Python:
```python
from apps.support.whatsapp_service import whatsapp_service

# Verificar configuração
print(f"URL: {whatsapp_service.base_url}")
print(f"Instância: {whatsapp_service.instance_name}")

# Verificar conexão
result = whatsapp_service.check_connection()
print(result)

# Enviar mensagem de teste (APÓS CONECTAR O WHATSAPP)
result = whatsapp_service.send_welcome_message(
    phone='5561998311920',  # Seu número
    name='Teste Sistema'
)
print(result)
```

### Testar Formulário (após conectar WhatsApp)
```powershell
$lead = @{
    nome_completo = "João Teste PowerShell"
    email = "joao@teste.com"
    telefone = "61998311920"
    estado = "DF"
    cidade = "Brasília"
    servico = "Teste WhatsApp"
    origem = "popup"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/support/capturar-lead/" -Method POST -Headers @{"Content-Type"="application/json"} -Body $lead
```

Resposta esperada:
```
success      : True
message      : Lead capturado com sucesso!
lead_id      : 1
whatsapp_sent: True
```

---

## 🔍 Troubleshooting

### Verificar se containers estão rodando
```powershell
docker-compose ps
```

### Ver logs da Evolution API
```powershell
docker-compose logs -f evolution-api
```

### Ver logs do Django
```powershell
docker-compose logs -f web
```

### Reiniciar Evolution API
```powershell
docker-compose restart evolution-api
```

### Reiniciar tudo
```powershell
docker-compose restart
```

---

## 🎯 Passo a Passo Completo

### 1. ✅ Instância criada (FEITO)
```
Nome: vetorial-local
ID: 32a7d394-0f65-4ef4-8596-35f34ccb9032
Status: close (aguardando conexão)
```

### 2. 📱 Conectar WhatsApp (PRÓXIMO PASSO)

**Opção A - Interface Web (mais fácil):**
1. Abra: http://localhost:8080
2. Encontre `vetorial-local` na lista
3. Clique em "Connect" ou QR Code
4. Escaneie com WhatsApp no celular

**Opção B - PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/connect/vetorial-local" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### 3. ✅ Verificar Conexão
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/connectionState/vetorial-local" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

Deve retornar: `state: open`

### 4. 🧪 Testar Envio
```powershell
# Teste direto via Evolution API
$msg = @{number="5561998311920"; text="Teste!"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/message/sendText/vetorial-local" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="B6D711FCDE4D4FD5936544120E713976"} -Body $msg

# Teste via Django (formulário)
$lead = @{nome_completo="Teste"; email="teste@email.com"; telefone="61998311920"; estado="DF"; cidade="Brasília"; servico="Teste"; origem="popup"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/support/capturar-lead/" -Method POST -Headers @{"Content-Type"="application/json"} -Body $lead
```

---

## 📋 Informações Importantes

**API Key:** `B6D711FCDE4D4FD5936544120E713976`  
**Instância:** `vetorial-local`  
**Evolution API:** http://localhost:8080  
**Django:** http://localhost:8000  
**Staff Dashboard:** http://localhost:8000/support/dashboard/

---

## ⚠️ Lembre-se

1. **Sempre use PowerShell**, não Bash/Linux commands
2. **QR Code expira em 30 segundos** - gere novo se necessário
3. **Status "open"** significa WhatsApp conectado
4. **Status "close"** significa aguardando conexão

---

## 🎉 Está Pronto!

Acesse **http://localhost:8080** e conecte seu WhatsApp agora! 📱
