import os
import django
from django.conf import settings
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')
django.setup()

from apps.support.models import Chamado, Cliente

print("Debug Chamados:")
try:
    chamados = Chamado.objects.all().select_related('cliente__user').order_by('-data_criacao')
    print(f"Total Chamados: {chamados.count()}")
    for c in chamados:
        try:
            print(f"#{c.id} - {c.titulo} - {c.cliente.user.email} - Prioridade: {c.prioridade}")
        except Exception as e:
            print(f"Error printing chamado #{c.id}: {e}")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
