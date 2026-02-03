
import os
import django
import sys

# Setup Django environment
sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestao360_project.settings")
django.setup()

from apps.services.models import Plano

print("--- DIAGNOSTIC START ---")
all_plans = Plano.objects.all()
print(f"Total Plans: {all_plans.count()}")

for p in all_plans:
    print(f"ID: {p.id} | Name: '{p.nome}' | Cat: '{p.categoria}' | Active: {p.ativo}")

mei_plans = Plano.objects.filter(ativo=True, categoria='mei')
print(f"MEI Filter Count: {mei_plans.count()}")
print("--- DIAGNOSTIC END ---")
