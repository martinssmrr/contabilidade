import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')
django.setup()

from apps.services.models import Plan, Plano

print(f"Plan count: {Plan.objects.count()}")
print(f"Plano count: {Plano.objects.count()}")

print("\n--- Planos (features/marketing) ---")
for p in Plano.objects.all():
    print(f"ID: {p.id} | Nome: {p.nome} | Cat: {p.categoria}")

print("\n--- Plans (subscription link) ---")
for p in Plan.objects.all():
    print(f"ID: {p.id} | Nome: {p.nome}")
