import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.support.models import Cliente

User = get_user_model()

print("--- DEBUG CLIENTS ---")
clientes = User.objects.filter(is_staff=False, is_active=True).order_by('first_name')
print(f"Total clients found: {clientes.count()}")

data = []
for cliente in clientes:
    fase = 'N/A'
    try:
        if hasattr(cliente, 'cliente_profile'):
            fase = cliente.cliente_profile.fase_abertura
    except Exception as e:
        print(f"Error accessing profile for {cliente}: {e}")
        pass

    print(f"Client: {cliente.username} | Email: {cliente.email} | Fase: {fase}")
    
    data.append({
        'id': cliente.id,
        'nome': cliente.get_full_name() or cliente.username,
        'email': cliente.email,
        'fase': fase
    })

print(json.dumps(data, indent=2))
