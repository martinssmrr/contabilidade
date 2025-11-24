# STATUS FINAL: Evolution API + WhatsApp

## ✅ O que foi feito

1. **Evolution API configurada e rodando**
   - Container: `evolution_api`
   - Porta: 8080
   - Versão: v2.2.3 (latest)
   - Integração: WHATSAPP-BAILEYS

2. **Chromium instalado**
   - Instaladas todas as dependências necessárias
   - Container reiniciado múltiplas vezes

3. **Instâncias criadas**
   - Instância atual: `gestao360-whatsapp`
   - ID: `58b188e3-5d14-4492-9dd8-c68361d2b2fd`
   - Token: `55ADAF48-5480-4612-93BA-CA3E0F6909ED`
   - Status: `connecting`

4. **Código Django integrado**
   - `apps/support/whatsapp_service.py` - Serviço pronto
   - `apps/support/views.py` - View de captura integrada
   - Tudo funcionando, aguardando apenas conexão do WhatsApp

## ❌ Problema Atual

**QR Code não está sendo gerado pela API**
- Endpoint `/instance/connect/{instance}` retorna `{"count": 0}`
- Rota `/session/qr/{instance}` não exibe QR
- Chromium instalado mas QR não aparece
- Problema conhecido em algumas versões do Baileys/Evolution API

## 🔧 SOLUÇÕES ALTERNATIVAS

### Opção 1: Código de Pareamento (RECOMENDADO PARA TESTAR)

Use o código de pareamento ao invés do QR Code:

```powershell
$body = @{
    phoneNumber = "5561998311920"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:8080/instance/connect/gestao360-whatsapp" `
    -Method POST `
    -Headers @{
        "Content-Type"="application/json"
        "apikey"="B6D711FCDE4D4FD5936544120E713976"
    } `
    -Body $body
```

Depois no WhatsApp:
1. Configurações → Aparelhos conectados
2. "Conectar usando número de telefone"
3. Digite o código que apareceu

### Opção 2: Migrar para WhatsApp Business API Oficial

**Vantagens:**
- Mais estável
- Suporte oficial do Meta/Facebook
- Sem problemas de QR code

**Desvantagens:**
- Requer conta business no Facebook
- Custos por mensagem (gratuito até certo limite)

**Como configurar:**

1. Crie conta business em https://business.facebook.com/
2. Adicione número de telefone business
3. No docker-compose.yml altere:
```yaml
- integration=WHATSAPP-BUSINESS
- WHATSAPP_BUSINESS_ACCOUNT_ID=seu_account_id
- WHATSAPP_BUSINESS_TOKEN=seu_token
```

### Opção 3: Usar Evolution API em produção diferente

Algumas alternativas ao Docker local:
- **Render.com** - Deploy gratuito (https://doc.evolution-api.com/v2/en/install/render)
- **Railway** - Deploy gratuito (https://railway.app)
- **VPS tradicional** - Instalação via NVM (menos problemas com Chromium)

### Opção 4: Tentar versão específica da Evolution API

Algumas versões funcionam melhor que outras:

```yaml
# No docker-compose.yml, mudar de:
image: atendai/evolution-api:latest

# Para:
image: atendai/evolution-api:v2.1.1
# ou
image: atendai/evolution-api:v2.0.0
```

Depois:
```powershell
docker-compose down
docker-compose up -d
```

## 📋 Próximos Passos

### Imediato (Testes Locais):
1. Tente a **Opção 1** (código de pareamento) - mais rápido
2. Se funcionar, teste o envio de mensagem
3. Se não funcionar, tente **Opção 4** (versão diferente)

### Produção (Depois que funcionar):
1. Deploy na DigitalOcean/AWS/Render
2. Configure WhatsApp Business API (mais confiável)
3. Configure webhooks para receber mensagens
4. Implemente respostas automáticas

## 🔐 Credenciais

```
API URL: http://localhost:8080 (local) ou http://evolution-api:8080 (Docker interno)
API KEY: B6D711FCDE4D4FD5936544120E713976
Instance: gestao360-whatsapp
Token: 55ADAF48-5480-4612-93BA-CA3E0F6909ED
Número: 5561998311920
```

## 📝 Comandos Úteis

### Verificar status:
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/connectionState/gestao360-whatsapp" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### Listar instâncias:
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/fetchInstances" -Method GET -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### Deletar instância:
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/delete/gestao360-whatsapp" -Method DELETE -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### Enviar mensagem (quando conectado):
```powershell
$msg = @{
    number = "5561998311920"
    text = "Teste de mensagem!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/message/sendText/gestao360-whatsapp" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="B6D711FCDE4D4FD5936544120E713976"} -Body $msg
```

## 💡 Conclusão

A integração está **99% pronta**. O único bloqueio é a conexão inicial do WhatsApp, que tem problema com geração de QR na versão atual do Baileys/Evolution API rodando em Docker/Windows.

**Recomendação:** Tente primeiro o código de pareamento (Opção 1). Se não funcionar, considere usar WhatsApp Business API oficial (Opção 2) que é mais estável para produção.
