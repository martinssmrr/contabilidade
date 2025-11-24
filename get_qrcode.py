import requests
import base64
import time
from PIL import Image
from io import BytesIO
import os

# Usar evolution-api quando dentro do Docker, localhost quando fora
API_URL = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
API_KEY = "B6D711FCDE4D4FD5936544120E713976"
INSTANCE = "vetorial-local"

headers = {"apikey": API_KEY}

print("Conectando e gerando QR Code...")
print("Aguarde alguns segundos...\n")

# Tentar várias vezes
for i in range(10):
    try:
        response = requests.get(
            f"{API_URL}/instance/connect/{INSTANCE}",
            headers=headers,
            timeout=10
        )
        
        data = response.json()
        print(f"Tentativa {i+1}: {data}")
        
        # Se tiver base64
        if isinstance(data, dict) and data.get('base64'):
            print("\n✅ QR Code obtido!")
            qr_base64 = data['base64']
            
            # Remover prefixo se houver
            if 'base64,' in qr_base64:
                qr_base64 = qr_base64.split('base64,')[1]
            
            # Decodificar e salvar
            qr_bytes = base64.b64decode(qr_base64)
            image = Image.open(BytesIO(qr_bytes))
            image.save('qrcode_whatsapp.png')
            print(f"✅ QR Code salvo em: qrcode_whatsapp.png")
            print("\nAbra o arquivo 'qrcode_whatsapp.png' e escaneie com WhatsApp!")
            print("WhatsApp → Configurações → Aparelhos conectados → Conectar aparelho")
            break
            
        # Se tiver código de pareamento
        elif isinstance(data, dict) and data.get('pairingCode'):
            print(f"\n✅ Código de pareamento: {data['pairingCode']}")
            print("Digite este código no WhatsApp!")
            break
            
        elif isinstance(data, dict) and data.get('code') == 'qrcode.not.found':
            print(f"QR Code ainda não gerado, aguardando...")
            time.sleep(3)
            continue
            
        time.sleep(2)
        
    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(2)

print("\nSe não funcionou, tente reiniciar a instância:")
print('Invoke-RestMethod -Uri "http://localhost:8080/instance/restart/vetorial-local" -Method PUT -Headers @{"apikey"="B6D711FCDE4D4FD5936544120E713976"}')
