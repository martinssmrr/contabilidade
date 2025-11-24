# SOLUÇÃO: QR Code não está gerando via API

## Problema
O endpoint `/instance/connect/{instance}` retorna `{"count": 0}` e o QR code não é gerado.

## Soluções Alternativas

### Opção 1: Interface Web do Evolution Manager (RECOMENDADO)
1. Acesse: http://localhost:8080/manager
2. Faça login com a API KEY: `B6D711FCDE4D4FD5936544120E713976`
3. Procure a instância `vetorial-local`
4. Clique no botão de conectar/QR Code
5. Escaneie com WhatsApp

### Opção 2: Usar WhatsApp Business API Oficial
Se o Baileys continuar com problemas, podemos migrar para a API oficial:
- Requer conta business no Facebook
- Mais estável mas com custos por mensagem
- Configuração no docker-compose: `integration: WHATSAPP-BUSINESS`

### Opção 3: Executar Evolution API em modo não-Docker
Algumas vezes o QR funciona melhor quando executado diretamente:
```bash
npm install -g @evolution/api
evolution-api start
```

### Opção 4: Usar código de pareamento (alternativa ao QR)
```powershell
# Solicitar código de pareamento para seu número
$body = @{
    phoneNumber = "5561998311920"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/instance/connect/vetorial-local" `
    -Method POST `
    -Headers @{
        "Content-Type"="application/json"
        "apikey"="B6D711FCDE4D4FD5936544120E713976"
    } `
    -Body $body
```

Depois digite o código no WhatsApp: Configurações → Aparelhos conectados → Conectar usando número

## Debugging

### Verificar se a instância está funcionando:
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/instance/connectionState/vetorial-local" `
    -Method GET `
    -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}
```

### Ver logs detalhados:
```powershell
docker-compose logs evolution-api --tail=200 | Select-String -Pattern "qr|connect|baileys" -Context 2
```

### Reiniciar completamente a Evolution API:
```powershell
docker-compose restart evolution-api
Start-Sleep -Seconds 10
```

## Próximos Passos

1. **IMEDIATO**: Tente http://localhost:8080/manager (interface web)
2. **SE NÃO FUNCIONAR**: Use código de pareamento (Opção 4)
3. **ÚLTIMA OPÇÃO**: Migrar para WhatsApp Business API oficial

## Informações da Instância Atual
- Nome: `vetorial-local`
- ID: `4888c2e0-d439-473a-b7c1-f3a42164287b`
- Token: `AD355106-9427-498C-BDD1-33271C2C28DD`
- Status: `close` (aguardando conexão)
- Integration: `WHATSAPP-BAILEYS`

## Notas
- O erro `count: 0` é comum em algumas versões do Baileys
- A interface web geralmente funciona mesmo quando a API não gera o QR
- Se tudo falhar, podemos tentar uma versão diferente da Evolution API
