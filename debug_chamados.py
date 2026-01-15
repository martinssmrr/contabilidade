import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.support.models import Chamado, Cliente

User = get_user_model()

try:
    user = User.objects.get(email='martinssmrr@gmail.com')
    print(f"User found: {user.username} (ID: {user.id})")
    
    try:
        cliente = user.cliente_profile
        print(f"Cliente profile found: {cliente} (ID: {cliente.id})")
        
        chamados = Chamado.objects.filter(cliente=cliente)
        print(f"Chamados count: {chamados.count()}")
        for c in chamados:
            print(f" - Chamado #{c.id}: {c.titulo} ({c.status})")
            
    except Cliente.DoesNotExist:
        print("Cliente profile NOT found for this user.")
        
except User.DoesNotExist:
    print("User with email martinssmrr@gmail.com NOT found.")
