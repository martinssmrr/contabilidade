import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.documents.models_guia_imposto import GuiaImposto

User = get_user_model()

print("=== Usuários ===")
for u in User.objects.all():
    print(f"ID: {u.id} | Username: {u.username} | Email: {u.email} | Nome: {u.first_name}")

print("\n=== Guias de Imposto ===")
guias = GuiaImposto.objects.all()
if not guias.exists():
    print("Nenhuma guia encontrada no banco de dados.")
else:
    for g in guias:
        print(f"ID: {g.id} | Cliente: {g.cliente.username} (ID: {g.cliente.id}) | Tipo: {g.tipo} | Vencimento: {g.vencimento}")

print("\n=== Verificação ===")
# Tenta simular o que a view faz para o primeiro usuário que encontrar
first_user = User.objects.first()
if first_user:
    guias_user = GuiaImposto.objects.filter(cliente=first_user)
    print(f"Guias para o usuário {first_user.username}: {guias_user.count()}")
