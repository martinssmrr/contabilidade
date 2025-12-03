#!/usr/bin/env python
"""Script para verificar e reenviar notificações pendentes."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao360_project.settings')
django.setup()

from apps.documents.models import DocumentoCliente
from apps.documents.tasks import enviar_email_notificacao_documento

# Verificar documentos pendentes
pendentes = DocumentoCliente.objects.filter(notificacao_enviada=False)
total = pendentes.count()

print(f"📊 Documentos pendentes: {total}")

if total > 0:
    print("\nDocumentos:")
    for doc in pendentes:
        print(f"  - ID {doc.id}: {doc.titulo}")
        print(f"    Cliente: {doc.cliente.email}")
        print(f"    Data: {doc.data_envio}")
    
    print("\n🚀 Reenviando notificações...")
    for doc in pendentes:
        enviar_email_notificacao_documento.delay(doc.id)
        print(f"  ✅ Task agendada para documento ID {doc.id}")
    
    print(f"\n✅ {total} tasks agendadas no Celery!")
else:
    print("✅ Não há documentos pendentes!")
    
    # Mostrar documentos enviados
    enviados = DocumentoCliente.objects.filter(notificacao_enviada=True)
    print(f"\n📧 Total de notificações enviadas: {enviados.count()}")
