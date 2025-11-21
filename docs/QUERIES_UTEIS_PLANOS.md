# 🔍 Queries Úteis - Sistema de Planos

Coleção de queries Django ORM úteis para gerenciar o sistema de planos.

---

## 📊 Consultas Básicas

### Listar todos os planos ativos
```python
from apps.services.models import Plano

planos_ativos = Plano.objects.filter(ativo=True)
for plano in planos_ativos:
    print(f"{plano.nome} - R$ {plano.preco}")
```

### Buscar plano por nome e categoria
```python
plano_prata = Plano.objects.get(nome='Prata', categoria='servicos')
print(plano_prata.descricao)
```

### Contar planos por categoria
```python
from django.db.models import Count

resultado = Plano.objects.values('categoria').annotate(total=Count('id'))
for item in resultado:
    print(f"{item['categoria']}: {item['total']} planos")
```

---

## 💰 Queries de Preços

### Planos com desconto
```python
planos_promocao = Plano.objects.exclude(preco_antigo__isnull=True)
for plano in planos_promocao:
    desconto = plano.percentual_desconto()
    economia = plano.preco_antigo - plano.preco
    print(f"{plano.nome}: {desconto}% OFF - Economize R$ {economia}")
```

### Plano mais caro e mais barato por categoria
```python
# Mais caro
mais_caro = Plano.objects.filter(categoria='servicos').order_by('-preco').first()
print(f"Mais caro: {mais_caro.nome} - R$ {mais_caro.preco}")

# Mais barato
mais_barato = Plano.objects.filter(categoria='servicos').order_by('preco').first()
print(f"Mais barato: {mais_barato.nome} - R$ {mais_barato.preco}")
```

### Média de preços por categoria
```python
from django.db.models import Avg

medias = Plano.objects.values('categoria').annotate(media=Avg('preco'))
for item in medias:
    print(f"{item['categoria']}: R$ {item['media']:.2f}")
```

---

## 🎯 Queries de Destaque

### Planos em destaque
```python
destaques = Plano.objects.filter(destaque=True, ativo=True)
for plano in destaques:
    print(f"⭐ {plano.nome} ({plano.get_categoria_display()})")
```

### Remover destaque de todos
```python
Plano.objects.filter(destaque=True).update(destaque=False)
print("✅ Todos os destaques foram removidos")
```

### Definir novo destaque
```python
# Remove destaque anterior da categoria
Plano.objects.filter(categoria='servicos', destaque=True).update(destaque=False)

# Define novo destaque
plano = Plano.objects.get(nome='Ouro', categoria='servicos')
plano.destaque = True
plano.save()
print(f"✅ {plano.nome} agora está em destaque")
```

---

## 🔄 Atualizações em Massa

### Aplicar desconto em todos os planos
```python
from decimal import Decimal

for plano in Plano.objects.all():
    # Salvar preço atual como antigo (se não tiver)
    if not plano.preco_antigo:
        plano.preco_antigo = plano.preco
    
    # Aplicar 20% de desconto
    plano.preco = plano.preco * Decimal('0.8')
    plano.save()
    
    print(f"✅ {plano.nome}: R$ {plano.preco_antigo} → R$ {plano.preco}")
```

### Remover desconto (voltar ao preço normal)
```python
for plano in Plano.objects.exclude(preco_antigo__isnull=True):
    plano.preco = plano.preco_antigo
    plano.preco_antigo = None
    plano.save()
    print(f"✅ {plano.nome} voltou ao preço normal")
```

### Reordenar planos
```python
# Ordenar por preço crescente
planos = Plano.objects.filter(categoria='servicos').order_by('preco')
for idx, plano in enumerate(planos, start=1):
    plano.ordem = idx * 10  # 10, 20, 30...
    plano.save()
```

---

## 📈 Análises e Relatórios

### Planos mais selecionados (requer ProcessoAbertura)
```python
from django.db.models import Count
from apps.services.models import Plano, ProcessoAbertura

ranking = Plano.objects.annotate(
    total_vendas=Count('processoabertura')
).order_by('-total_vendas')

for idx, plano in enumerate(ranking, start=1):
    print(f"{idx}º - {plano.nome}: {plano.total_vendas} seleções")
```

### Receita total por plano
```python
from django.db.models import Sum

receitas = Plano.objects.annotate(
    receita_total=Sum('processoabertura__valor_pago')
).filter(receita_total__isnull=False)

for plano in receitas:
    print(f"{plano.nome}: R$ {plano.receita_total:.2f}")
```

### Taxa de conversão por plano
```python
from django.db.models import Count, Q

planos_com_stats = Plano.objects.annotate(
    total_visualizacoes=Count('processoabertura'),
    total_pagos=Count(
        'processoabertura',
        filter=Q(processoabertura__status='concluido')
    )
)

for plano in planos_com_stats:
    if plano.total_visualizacoes > 0:
        taxa = (plano.total_pagos / plano.total_visualizacoes) * 100
        print(f"{plano.nome}: {taxa:.1f}% de conversão")
```

---

## 🛠️ Operações Administrativas

### Criar novo plano via código
```python
novo_plano = Plano.objects.create(
    nome="Diamante",
    categoria="servicos",
    preco=999.90,
    preco_antigo=1299.90,
    descricao="Plano premium com todos os benefícios",
    features=[
        "Tudo do plano Ouro",
        "Consultoria personalizada",
        "Gerente exclusivo 24/7",
        "Relatórios customizados"
    ],
    mercadopago_price_id="",
    ativo=True,
    destaque=False,
    ordem=4
)
print(f"✅ Plano {novo_plano.nome} criado com sucesso!")
```

### Duplicar plano existente
```python
plano_original = Plano.objects.get(nome='Prata', categoria='servicos')

# Criar cópia
novo_plano = Plano.objects.create(
    nome=f"{plano_original.nome} Plus",
    categoria=plano_original.categoria,
    preco=plano_original.preco + 100,
    preco_antigo=None,
    descricao=plano_original.descricao,
    features=plano_original.features.copy(),  # Cópia da lista
    ativo=True,
    destaque=False,
    ordem=plano_original.ordem + 5
)
print(f"✅ Plano duplicado: {novo_plano.nome}")
```

### Desativar planos antigos
```python
from datetime import timedelta
from django.utils import timezone

# Desativar planos não atualizados há mais de 6 meses
seis_meses_atras = timezone.now() - timedelta(days=180)
planos_antigos = Plano.objects.filter(
    atualizado_em__lt=seis_meses_atras,
    ativo=True
)

for plano in planos_antigos:
    plano.ativo = False
    plano.save()
    print(f"🔒 {plano.nome} desativado (não atualizado desde {plano.atualizado_em})")
```

---

## 🔍 Queries Avançadas

### Planos com features específicas
```python
# Buscar planos que incluem "Certificado digital"
planos_com_certificado = Plano.objects.filter(
    features__contains=['Certificado digital incluído']
)

for plano in planos_com_certificado:
    print(f"✓ {plano.nome}")
```

### Planos sem integração com Mercado Pago
```python
sem_integracao = Plano.objects.filter(
    Q(mercadopago_price_id__isnull=True) | Q(mercadopago_price_id='')
)

print(f"⚠️ {sem_integracao.count()} planos sem integração MP:")
for plano in sem_integracao:
    print(f"  - {plano.nome} ({plano.categoria})")
```

### Validar consistência de dados
```python
# Verificar planos com preço antigo menor que atual (erro)
inconsistentes = Plano.objects.filter(
    preco_antigo__lt=models.F('preco')
).exclude(preco_antigo__isnull=True)

if inconsistentes.exists():
    print("❌ Planos com preço antigo inconsistente:")
    for plano in inconsistentes:
        print(f"  - {plano.nome}: Antigo R$ {plano.preco_antigo} < Atual R$ {plano.preco}")
else:
    print("✅ Todos os planos estão consistentes")
```

---

## 📊 Exportar Dados

### Exportar para CSV
```python
import csv
from django.http import HttpResponse

def exportar_planos_csv():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="planos.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nome', 'Categoria', 'Preço', 'Preço Antigo', 'Ativo', 'Features'])
    
    for plano in Plano.objects.all():
        writer.writerow([
            plano.nome,
            plano.get_categoria_display(),
            plano.preco,
            plano.preco_antigo or '',
            'Sim' if plano.ativo else 'Não',
            ' | '.join(plano.features)
        ])
    
    return response
```

### Exportar para JSON
```python
import json

planos_data = []
for plano in Plano.objects.filter(ativo=True):
    planos_data.append({
        'id': plano.id,
        'nome': plano.nome,
        'categoria': plano.categoria,
        'preco': float(plano.preco),
        'preco_antigo': float(plano.preco_antigo) if plano.preco_antigo else None,
        'descricao': plano.descricao,
        'features': plano.features,
        'destaque': plano.destaque,
    })

with open('planos_ativos.json', 'w', encoding='utf-8') as f:
    json.dump(planos_data, f, ensure_ascii=False, indent=2)

print(f"✅ {len(planos_data)} planos exportados para planos_ativos.json")
```

---

## 🧪 Queries de Teste

### Popular banco de testes
```python
from decimal import Decimal

categorias = ['servicos', 'comercio', 'abertura']
nomes = ['Bronze', 'Prata', 'Ouro']
ordem = 1

for categoria in categorias:
    for idx, nome in enumerate(nomes):
        preco = Decimal(200 + (idx * 150))
        Plano.objects.create(
            nome=nome,
            categoria=categoria,
            preco=preco,
            preco_antigo=preco * Decimal('1.3'),
            descricao=f"Plano {nome} para {categoria}",
            features=[f"Feature {i+1}" for i in range(5)],
            ativo=True,
            destaque=(idx == 1),  # Prata em destaque
            ordem=ordem
        )
        ordem += 1

print(f"✅ {Plano.objects.count()} planos de teste criados")
```

### Limpar dados de teste
```python
Plano.objects.all().delete()
print("✅ Todos os planos foram removidos")
```

---

## 💡 Dicas de Performance

### Use `select_related` para ForeignKeys
```python
# Ruim (N+1 queries)
processos = ProcessoAbertura.objects.all()
for p in processos:
    print(p.plano_selecionado.nome)  # Query por iteração

# Bom (2 queries total)
processos = ProcessoAbertura.objects.select_related('plano_selecionado')
for p in processos:
    print(p.plano_selecionado.nome)  # Sem query adicional
```

### Use `only()` para limitar campos
```python
# Buscar apenas nome e preço
planos = Plano.objects.only('nome', 'preco')
for plano in planos:
    print(f"{plano.nome}: R$ {plano.preco}")
```

### Use `values()` para dicionários
```python
# Mais rápido que criar objetos completos
planos_dict = Plano.objects.filter(ativo=True).values('nome', 'preco', 'categoria')
for plano in planos_dict:
    print(f"{plano['nome']}: R$ {plano['preco']}")
```

---

## 🚀 Como Usar

### No Shell Django:
```bash
docker-compose exec web python manage.py shell
```

Depois copie e cole as queries desejadas.

### Em Views:
```python
def minha_view(request):
    # Cole a query aqui
    planos = Plano.objects.filter(ativo=True)
    return render(request, 'template.html', {'planos': planos})
```

### Em Scripts:
Crie um arquivo em `scripts/` e execute com:
```bash
docker-compose exec web python scripts/meu_script.py
```

---

**📚 Mais informações:**
- [Django QuerySet API](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- [Django Aggregation](https://docs.djangoproject.com/en/stable/topics/db/aggregation/)
- [Documentação do Projeto](./SISTEMA_PLANOS_DINAMICOS.md)
