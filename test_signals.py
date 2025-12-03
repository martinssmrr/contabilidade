"""
Script para testar se signals estão funcionando.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao360_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.documents.models import NotaFiscal, DocumentoEmpresa
from apps.users.models import CertidaoNegativa
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

print("\n=== TESTANDO SIGNALS ===\n")

# 1. Verificar se há clientes com e-mail
clientes = User.objects.filter(email__isnull=False).exclude(email='').exclude(is_staff=True)
print(f"Clientes com e-mail cadastrado: {clientes.count()}")

for cliente in clientes[:5]:
    print(f"  - ID: {cliente.id}, User: {cliente.username}, Email: {cliente.email}")

if not clientes.exists():
    print("\n⚠️  ERRO: Nenhum cliente com e-mail cadastrado!")
    print("   Cadastre um e-mail em um cliente no Django Admin.\n")
    exit(1)

# 2. Verificar se há staff users
staff_users = User.objects.filter(is_staff=True)
print(f"\nStaff users disponíveis: {staff_users.count()}")

if not staff_users.exists():
    print("\n⚠️  ERRO: Nenhum staff user encontrado!")
    exit(1)

staff = staff_users.first()
cliente = clientes.first()

print(f"\n=== TESTE 1: Criar NotaFiscal ===")
print(f"Cliente: {cliente.username} ({cliente.email})")
print(f"Staff: {staff.username}")

# Criar arquivo fake
arquivo = SimpleUploadedFile("nota_fiscal_teste.pdf", b"conteudo fake", content_type="application/pdf")

try:
    nf = NotaFiscal.objects.create(
        cliente=cliente,
        arquivo_pdf=arquivo,
        enviado_por=staff,
        observacoes="Teste de signal automático"
    )
    print(f"✅ NotaFiscal criada: ID {nf.id}")
    print("   Aguarde alguns segundos e verifique os logs do Celery...")
    print(f"   docker-compose logs web | Select-String 'NotaFiscal {nf.id}'")
except Exception as e:
    print(f"❌ Erro ao criar NotaFiscal: {e}")

print("\n=== FIM DOS TESTES ===\n")
