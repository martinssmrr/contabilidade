"""
Script para testar upload via API do painel staff.
Simula o que acontece quando staff faz upload pelo dashboard.
"""
import os
import django
import requests
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao360_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

print("\n=== TESTE DE UPLOAD VIA PAINEL STAFF ===\n")

# 1. Verificar clientes e staff
clientes = User.objects.filter(email__isnull=False).exclude(email='').exclude(is_staff=True)
staff_users = User.objects.filter(is_staff=True)

if not clientes.exists():
    print("❌ Nenhum cliente com e-mail!")
    exit(1)

if not staff_users.exists():
    print("❌ Nenhum staff user!")
    exit(1)

cliente = clientes.first()
staff = staff_users.first()

print(f"Cliente: {cliente.username} ({cliente.email})")
print(f"Staff: {staff.username}\n")

# 2. Simular POST para API de Nota Fiscal
print("=== TESTE 1: Upload de Nota Fiscal via API ===")

# Criar client Django
client = Client()
client.force_login(staff)

# Criar arquivo fake
arquivo = SimpleUploadedFile(
    "nota_fiscal_teste.pdf",
    b"PDF fake content",
    content_type="application/pdf"
)

# Fazer POST para API
response = client.post(
    '/support/api/nota-fiscal/enviar/',
    {
        'cliente_id': cliente.id,
        'arquivo_pdf': arquivo,
        'observacoes': 'Teste via API'
    },
    format='multipart'
)

print(f"Status: {response.status_code}")
print(f"Response: {response.content.decode() if response.content else 'Sem conteúdo'}")

if response.status_code == 200 or response.status_code == 302:
    print("✅ Upload via API simulado com sucesso!")
    print("📧 Verifique os logs para confirmar se signal disparou e e-mail foi enviado.")
    print("\nComando para verificar logs:")
    print("docker-compose logs --tail=100 web | Select-String -Pattern 'Signal|Task|Notificação'")
else:
    print(f"❌ Erro no upload: {response.status_code}")

print("\n=== FIM DO TESTE ===\n")
