#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')
django.setup()

from apps.services.models import Plano

print("=== TODOS OS PLANOS ===")
for p in Plano.objects.all():
    print(f"ID={p.id}, nome={p.nome}, ativo={p.ativo} (type={type(p.ativo).__name__}), categoria='{p.categoria}'")

print("\n=== FILTRO: ativo=True, categoria='servicos' ===")
servicos = Plano.objects.filter(ativo=True, categoria='servicos')
print(f"Count: {servicos.count()}")
for p in servicos:
    print(f"  - {p.nome}")

print("\n=== FILTRO: ativo=True, categoria='comercio' ===")
comercio = Plano.objects.filter(ativo=True, categoria='comercio')
print(f"Count: {comercio.count()}")
for p in comercio:
    print(f"  - {p.nome}")
