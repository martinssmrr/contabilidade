#!/usr/bin/env python
"""
Teste rápido para verificar se os planos estão sendo passados para o template
"""
import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')
django.setup()

from django.test import RequestFactory
from vetorial_project.urls import home_view
from apps.services.models import Plano

print("=" * 60)
print("TESTE - Sistema de Planos")
print("=" * 60)

# Verificar planos no banco
print(f"\n✅ Planos no banco: {Plano.objects.count()}")
print(f"   - Serviços: {Plano.objects.filter(categoria='servicos').count()}")
print(f"   - Comércio: {Plano.objects.filter(categoria='comercio').count()}")
print(f"   - Abertura: {Plano.objects.filter(categoria='abertura').count()}")

# Testar view
print("\n📊 Testando view home_view...")
rf = RequestFactory()
request = rf.get('/')
response = home_view(request)

print(f"   Status Code: {response.status_code}")

# Verificar context
if hasattr(response, 'context_data'):
    context = response.context_data
    print(f"\n✅ Context tem {len(context)} itens")
    
    if 'planos_servicos' in context:
        print(f"   ✅ planos_servicos: {context['planos_servicos'].count()} planos")
        for p in context['planos_servicos']:
            print(f"      - {p.nome} (R$ {p.preco})")
    else:
        print("   ❌ planos_servicos NÃO está no context!")
    
    if 'planos_comercio' in context:
        print(f"   ✅ planos_comercio: {context['planos_comercio'].count()} planos")
        for p in context['planos_comercio']:
            print(f"      - {p.nome} (R$ {p.preco})")
    else:
        print("   ❌ planos_comercio NÃO está no context!")
else:
    print("   ❌ Response não tem context_data!")
    print(f"   Type: {type(response)}")
    print(f"   Dir: {[x for x in dir(response) if not x.startswith('_')]}")

print("\n" + "=" * 60)
