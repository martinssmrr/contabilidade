from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from apps.services.models import Subscription
from apps.payments.models import Payment
from apps.support.models import Ticket
from apps.documents.models import Document

# Create your views here.

@login_required
def dashboard_index(request):
    """
    View principal do dashboard.
    Redireciona para diferentes dashboards baseado no role do usuário.
    """
    user = request.user
    
    context = {
        'user': user,
    }
    
    # Dashboard para clientes
    if user.role == 'cliente':
        context.update({
            'assinaturas': Subscription.objects.filter(cliente=user),
            'pagamentos': Payment.objects.filter(cliente=user).order_by('-criado_em')[:5],
            'tickets': Ticket.objects.filter(cliente=user).order_by('-criado_em')[:5],
            'documentos': Document.objects.filter(usuario=user).order_by('-criado_em')[:5],
        })
        return render(request, 'dashboard/cliente.html', context)
    
    # Dashboard para contador
    elif user.role == 'contador':
        context.update({
            'total_clientes': Count('id'),
            'tickets_abertos': Ticket.objects.filter(
                staff_designado=user, 
                status='aberto'
            ).count(),
            'tickets_em_andamento': Ticket.objects.filter(
                staff_designado=user,
                status='em_andamento'
            ).count(),
        })
        return render(request, 'dashboard/contador.html', context)
    
    # Dashboard para admin
    elif user.role == 'admin':
        context.update({
            'total_clientes': Payment.objects.filter(tipo='cliente').count(),
            'total_receita': Payment.objects.filter(
                status='aprovado'
            ).aggregate(Sum('valor'))['valor__sum'] or 0,
            'assinaturas_ativas': Subscription.objects.filter(
                status='ativa'
            ).count(),
            'tickets_pendentes': Ticket.objects.filter(
                status='aberto'
            ).count(),
        })
        return render(request, 'dashboard/admin.html', context)
    
    # Dashboard para suporte
    elif user.role == 'suporte':
        context.update({
            'meus_tickets': Ticket.objects.filter(
                staff_designado=user
            ).order_by('-criado_em')[:10],
            'tickets_abertos': Ticket.objects.filter(
                status='aberto'
            ).count(),
        })
        return render(request, 'dashboard/suporte.html', context)
    
    # Fallback para usuários sem role definido
    return render(request, 'dashboard/default.html', context)
