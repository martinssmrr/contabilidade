import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')
django.setup()

from apps.services.models import Plano

print("--- Checking Planos ---")
planos = Plano.objects.all()
for p in planos:
    print(f"ID: {p.id}, Nome: {p.nome}, Categoria: '{p.categoria}', Ativo: {p.ativo}")

print("\n--- Checking Filter for MEI ---")
mei_planos = Plano.objects.filter(ativo=True, categoria='mei')
print(f"Count: {mei_planos.count()}")
for p in mei_planos:
    print(f"Found: {p.nome}")
