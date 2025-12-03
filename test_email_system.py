#!/usr/bin/env python
"""Script para testar o envio automático de e-mail."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao360_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.documents.models import DocumentoCliente
from django.core.files.base import ContentFile
import time

User = get_user_model()

# Pegar um cliente (não staff)
cliente = User.objects.filter(is_staff=False).first()

if not cliente:
    print("❌ Nenhum cliente encontrado! Crie um usuário cliente primeiro.")
    exit(1)

if not cliente.email:
    print(f"❌ Cliente '{cliente.username}' não tem e-mail cadastrado!")
    exit(1)

print(f"🧪 Criando documento de teste...")
print(f"   Cliente: {cliente.username} ({cliente.email})")

# Criar documento de teste
doc = DocumentoCliente.objects.create(
    cliente=cliente,
    tipo_documento='outros',
    titulo='TESTE - Documento de Verificação do Sistema',
    descricao='Este é um documento de teste para verificar se o sistema de notificação está funcionando corretamente.',
    enviado_por=User.objects.filter(is_staff=True).first()
)

# Adicionar um arquivo fake
doc.arquivo.save('teste.pdf', ContentFile(b'Arquivo de teste'), save=True)

print(f"✅ Documento criado! ID: {doc.id}")
print(f"\n⏳ Aguardando 5 segundos para o Celery processar...")

time.sleep(5)

# Verificar se foi enviado
doc.refresh_from_db()

print(f"\n📊 Status:")
print(f"   Notificação enviada: {'✅ SIM' if doc.notificacao_enviada else '❌ NÃO'}")
if doc.data_notificacao:
    print(f"   Data de envio: {doc.data_notificacao}")

if doc.notificacao_enviada:
    print(f"\n🎉 SUCESSO! E-mail enviado para {cliente.email}")
else:
    print(f"\n⚠️ E-mail NÃO foi enviado. Verifique:")
    print(f"   1. Celery está rodando?")
    print(f"   2. Cliente tem e-mail válido?")
    print(f"   3. Verificar logs do Django")
