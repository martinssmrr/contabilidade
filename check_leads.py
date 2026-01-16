from apps.support.models import Lead
print(f"Total leads: {Lead.objects.count()}")
for lead in Lead.objects.all()[:5]:
    print(f"ID: {lead.id}, Nome: {lead.nome_completo}")
