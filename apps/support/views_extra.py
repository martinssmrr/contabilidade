
# ==================== GUIAS DE IMPOSTO ====================

@login_required
@user_passes_test(is_staff_user)
def api_guias_imposto_list(request):
    """Lista guias de imposto"""
    from apps.documents.models_guia_imposto import GuiaImposto
    guias = GuiaImposto.objects.select_related('cliente').all().order_by('-vencimento')
    data = []
    for guia in guias:
        data.append({
            'id': guia.id,
            'cliente_id': guia.cliente.id,
            'cliente_email': guia.cliente.email,
            'tipo': guia.get_tipo_display(),
            'descricao': guia.descricao or '',
            'valor': str(guia.valor),
            'vencimento': guia.vencimento.strftime('%d/%m/%Y'),
            'competencia': guia.competencia.strftime('%m/%Y'),
            'status': guia.get_status_display(),
            'status_raw': guia.status,
            'arquivo_url': guia.arquivo_pdf.url if guia.arquivo_pdf else None,
            'codigo_barras': guia.codigo_barras
        })
    return JsonResponse({'success': True, 'data': data})

@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_guia_imposto_enviar(request):
    """Envia uma guia de imposto"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    from apps.documents.models_guia_imposto import GuiaImposto
    
    try:
        cliente_id = request.POST.get('cliente_id')
        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor')
        vencimento = request.POST.get('vencimento')
        competencia = request.POST.get('competencia') # YYYY-MM-DD
        arquivo = request.FILES.get('arquivo')
        
        if not all([cliente_id, tipo, valor, vencimento, competencia, arquivo]):
            return JsonResponse({'success': False, 'error': 'Todos os campos são obrigatórios'}, status=400)
            
        cliente = get_object_or_404(User, pk=cliente_id)
        
        guia = GuiaImposto.objects.create(
            cliente=cliente,
            tipo=tipo,
            valor=valor,
            vencimento=vencimento,
            competencia=competencia,
            arquivo_pdf=arquivo,
            status='a_vencer'
        )
        
        return JsonResponse({'success': True, 'message': 'Guia enviada com sucesso!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# ==================== ASSINATURAS / PLANOS ====================

@login_required
@user_passes_test(is_staff_user)
def api_cliente_subscription_info(request, cliente_id):
    """Retorna informações da assinatura do cliente"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    from apps.services.models import Subscription, Plan
    
    cliente = get_object_or_404(User, pk=cliente_id)
    
    # Tenta pegar assinatura ativa
    sub = Subscription.objects.filter(cliente=cliente, status='ativa').first()
    
    # Se não tiver ativa, pega a última criada
    if not sub:
        sub = Subscription.objects.filter(cliente=cliente).order_by('-criado_em').first()
        
    data = {}
    if sub:
        data = {
            'plano_id': sub.plano.id,
            'plano_nome': sub.plano.nome,
            'status': sub.get_status_display(),
            'data_inicio': sub.data_inicio.strftime('%d/%m/%Y'),
            'valor': str(sub.plano.preco)
        }
    else:
        data = None # Explicitly showing no subscription
        
    # Listar todos os planos disponíveis para possível troca
    planos_disponiveis = []
    # Using Plan from services.models vs Plano? The Subscription model uses Plan.
    for p in Plan.objects.filter(ativo=True).order_by('preco'):
        planos_disponiveis.append({
            'id': p.id,
            'nome': p.nome,
            'preco': str(p.preco)
        })
        
    return JsonResponse({
        'success': True, 
        'data': data,
        'planos_disponiveis': planos_disponiveis
    })

@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_cliente_subscription_update(request):
    """Atualiza o plano do cliente"""
    from django.utils import timezone
    from django.contrib.auth import get_user_model
    from apps.services.models import Subscription, Plan
    
    User = get_user_model()
    
    cliente_id = request.POST.get('cliente_id')
    plano_id = request.POST.get('plano_id')
    
    try:
        cliente = get_object_or_404(User, pk=cliente_id)
        novo_plano = get_object_or_404(Plan, pk=plano_id)
        
        # Cancelar assinaturas anteriores
        Subscription.objects.filter(cliente=cliente, status='ativa').update(
            status='cancelada', 
            data_fim=timezone.now().date()
        )
        
        # Criar nova assinatura
        Subscription.objects.create(
            cliente=cliente,
            plano=novo_plano,
            status='ativa',
            data_inicio=timezone.now().date()
        )
        
        return JsonResponse({'success': True, 'message': 'Plano atualizado com sucesso!'})
    except Exception as e:
        logger.error(f"Erro ao atualizar plano: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
