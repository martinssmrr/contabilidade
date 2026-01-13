import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao360_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.documents.models import NotaFiscal, NotaFiscalCliente

User = get_user_model()

print("=== DIAGNÓSTICO NOTAS FISCAIS ===")

print(f"\nTotal de Usuários: {User.objects.count()}")
users = User.objects.all()
for u in users:
    print(f"ID: {u.id} | User: {u.username} | Email: {u.email} | Nome: {u.get_full_name()}")

print(f"\nTotal de Notas Fiscais (Recebidas/Admin): {NotaFiscal.objects.count()}")
nfs = NotaFiscal.objects.all()
for nf in nfs:
    print(f"NF ID: {nf.id} | Cliente ID: {nf.cliente_id} ({nf.cliente.username}) | Arquivo: {nf.arquivo_pdf.name}")

print(f"\nTotal de Notas Fiscais Clientes (Enviadas): {NotaFiscalCliente.objects.count()}")
nfcs = NotaFiscalCliente.objects.all()
for nfc in nfcs:
    print(f"NFC ID: {nfc.id} | Cliente ID: {nfc.cliente_id} ({nfc.cliente.username}) | Arquivo: {nfc.arquivo.name}")

print("\n=== FIM ===")
