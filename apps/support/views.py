from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.core.cache import cache
import json
import logging
from .models import Lead, Ticket, Cliente, Chamado, ChamadoAttachment, ChamadoMessage
from .forms import ChamadoForm, ChamadoMessageForm
from django.shortcuts import redirect
from apps.blog.models import Post, Category
from apps.testimonials.models import Testimonial
from apps.services.models import Plano
from apps.documents.models import Document
from .whatsapp_service import whatsapp_service

logger = logging.getLogger(__name__)

# Create your views here.

def is_staff_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_user)
def staff_dashboard(request):
    """
    Dashboard administrativa para gerenciamento de leads, tickets e envio de notas fiscais.
    """
    return render(request, 'staff/dashboard_new.html')

# ==================== LEADS API ====================

@login_required
@user_passes_test(is_staff_user)
def api_leads_list(request):
    """Lista todos os leads"""
    leads = Lead.objects.all().order_by('-criado_em')
    data = []
    for lead in leads:
        data.append({
            'id': lead.id,
            'nome_completo': lead.nome_completo,
            'email': lead.email,
            'telefone': lead.telefone,
            'estado': lead.estado,
            'cidade': lead.cidade,
            'servico_interesse': lead.servico_interesse,
            'origem': lead.origem,
            'contatado': lead.contatado,
            'observacoes': lead.observacoes or '',
            'criado_em': lead.criado_em.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'success': True, 'data': data})

@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_leads_create(request):
    """Cria um novo lead"""
    try:
        data = json.loads(request.body)
        lead = Lead.objects.create(
            nome_completo=data.get('nome_completo'),
            email=data.get('email'),
            telefone=data.get('telefone'),
            estado=data.get('estado'),
            cidade=data.get('cidade'),
            servico_interesse=data.get('servico_interesse'),
            origem=data.get('origem', 'popup'),
            contatado=data.get('contatado', False),
            observacoes=data.get('observacoes', '')
        )
        return JsonResponse({'success': True, 'id': lead.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_leads_update(request, pk):
    """Atualiza um lead existente"""
    try:
        lead = get_object_or_404(Lead, pk=pk)
        data = json.loads(request.body)
        
        lead.nome_completo = data.get('nome_completo', lead.nome_completo)
        lead.email = data.get('email', lead.email)
        lead.telefone = data.get('telefone', lead.telefone)
        lead.estado = data.get('estado', lead.estado)
        lead.cidade = data.get('cidade', lead.cidade)
        lead.servico_interesse = data.get('servico_interesse', lead.servico_interesse)
        contatado_val = data.get('contatado', lead.contatado)
        # Converter para booleano se vier como string
        if isinstance(contatado_val, str):
            contatado_val = contatado_val.lower() in ['true', '1', 'on']
        lead.contatado = bool(contatado_val)
        lead.observacoes = data.get('observacoes', lead.observacoes)
        
        lead.save()
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f'Erro ao atualizar lead {pk}: {str(e)} | Dados recebidos: {data}')
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE"])
def api_leads_delete(request, pk):
    """Deleta um lead"""
    try:
        lead = get_object_or_404(Lead, pk=pk)
        lead.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_leads_send_whatsapp(request, pk):
    """Envia mensagem via WhatsApp para um lead"""
    try:
        lead = get_object_or_404(Lead, pk=pk)
        data = json.loads(request.body)
        message = data.get('message', '')
        
        if not message:
            # Mensagem padrão se não for fornecida
            message = f"""Olá {lead.nome_completo}! 👋

Somos da Vetorial Contabilidade e vimos que você demonstrou interesse em nossos serviços de {lead.servico_interesse}.

Estamos à disposição para esclarecer qualquer dúvida e apresentar nossas soluções personalizadas para o seu negócio.

Podemos agendar uma conversa?"""
        
        # Enviar mensagem via WhatsApp
        success, response = whatsapp_service.send_custom_message(
            phone=lead.telefone,
            message=message
        )
        
        if success:
            # Marcar lead como contatado
            lead.contatado = True
            lead.save()
            
            logger.info(f"Mensagem WhatsApp enviada para lead {lead.id} - {lead.nome_completo}")
            return JsonResponse({
                'success': True, 
                'message': 'Mensagem enviada com sucesso!',
                'phone': lead.telefone
            })
        else:
            logger.warning(f"Falha ao enviar WhatsApp para lead {lead.id}: {response}")
            return JsonResponse({
                'success': False, 
                'error': 'Não foi possível enviar a mensagem. Verifique se o WhatsApp está conectado.'
            }, status=500)
            
    except Exception as e:
        logger.error(f"Erro ao enviar WhatsApp para lead {pk}: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# ==================== TICKETS API ====================

@login_required
@user_passes_test(is_staff_user)
def api_tickets_list(request):
    """Lista todos os tickets"""
    tickets = Ticket.objects.all().select_related('cliente', 'staff_designado').order_by('-criado_em')
    data = []
    for ticket in tickets:
        data.append({
            'id': ticket.id,
            'titulo': ticket.titulo,
            'descricao': ticket.descricao,
            'cliente': ticket.cliente.get_full_name() or ticket.cliente.username,
            'staff': ticket.staff_designado.get_full_name() if ticket.staff_designado else 'Não atribuído',
            'status': ticket.get_status_display(),
            'prioridade': ticket.get_prioridade_display(),
            'criado_em': ticket.criado_em.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'success': True, 'data': data})

# ==================== BLOG API ====================

@login_required
@user_passes_test(is_staff_user)
def api_posts_list(request):
    """Lista todos os posts do blog"""
    posts = Post.objects.all().select_related('author', 'category').order_by('-created_at')
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'category': post.category.name if post.category else 'Sem categoria',
            'author': post.author.get_full_name() or post.author.username,
            'status': post.get_status_display(),
            'is_featured': post.is_featured,
            'created_at': post.created_at.strftime('%Y-%m-%d')
        })
    return JsonResponse({'success': True, 'data': data})

@login_required
@user_passes_test(is_staff_user)
def api_categories_list(request):
    """Lista todas as categorias"""
    categories = Category.objects.all().order_by('name')
    data = []
    for cat in categories:
        data.append({
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'description': cat.description,
            'created_at': cat.created_at.strftime('%Y-%m-%d')
        })
    return JsonResponse({'success': True, 'data': data})

# ==================== TESTIMONIALS API ====================

@login_required
@user_passes_test(is_staff_user)
def api_testimonials_list(request):
    """Lista todos os depoimentos"""
    testimonials = Testimonial.objects.all().order_by('order', '-created_at')
    data = []
    for test in testimonials:
        data.append({
            'id': test.id,
            'name': test.name,
            'position': test.position,
            'content': test.content[:100] + '...' if len(test.content) > 100 else test.content,
            'is_active': test.is_active,
            'order': test.order,
            'created_at': test.created_at.strftime('%Y-%m-%d')
        })
    return JsonResponse({'success': True, 'data': data})

@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE"])
def api_testimonials_delete(request, pk):
    """Deleta um depoimento"""
    try:
        testimonial = get_object_or_404(Testimonial, pk=pk)
        testimonial.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# ==================== PLANOS API ====================

@login_required
@user_passes_test(is_staff_user)
def api_planos_list(request):
    """Lista todos os planos"""
    planos = Plano.objects.all().order_by('categoria', 'ordem')
    data = []
    for plano in planos:
        data.append({
            'id': plano.id,
            'nome': plano.nome,
            'categoria': plano.get_categoria_display(),
            'preco': str(plano.preco),
            'preco_antigo': str(plano.preco_antigo) if plano.preco_antigo else None,
            'descricao': plano.descricao,
            'ativo': plano.ativo,
            'destaque': plano.destaque,
            'ordem': plano.ordem
        })
    return JsonResponse({'success': True, 'data': data})

@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE"])
def api_planos_delete(request, pk):
    """Deleta um plano"""
    try:
        plano = get_object_or_404(Plano, pk=pk)
        plano.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# ==================== DOCUMENTS API ====================

@login_required
@user_passes_test(is_staff_user)
def api_documents_list(request):
    """Lista todos os documentos"""
    documents = Document.objects.all().select_related('usuario').order_by('-criado_em')
    data = []
    for doc in documents:
        data.append({
            'id': doc.id,
            'usuario': doc.usuario.get_full_name() or doc.usuario.username,
            'titulo': doc.titulo,
            'categoria': doc.get_categoria_display(),
            'visivel_para_cliente': doc.visivel_para_cliente,
            'criado_em': doc.criado_em.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'success': True, 'data': data})

@require_http_methods(["POST"])
@csrf_exempt
def capturar_lead(request):
    """
    View para capturar leads dos formulários do site (popup e seção de contato).
    Envia automaticamente uma mensagem de WhatsApp via Evolution API.
    Limite: cada telefone pode solicitar atendimento até 5 vezes.
    """
    try:
        data = json.loads(request.body)
        telefone = data.get('telefone')
        if not telefone:
            return JsonResponse({'success': False, 'message': 'Telefone obrigatório.'}, status=400)

        # Rate limiting: máximo 5 leads por telefone
        cache_key = f"lead_attempts_{telefone}"
        attempts = cache.get(cache_key, 0)
        if attempts >= 5:
            return JsonResponse({'success': False, 'message': 'Limite de solicitações atingido para este telefone.'}, status=429)
        cache.set(cache_key, attempts + 1, 60 * 60 * 24)  # Limite por 24h

        # Cria o lead no banco de dados
        lead = Lead.objects.create(
            nome_completo=data.get('nome_completo'),
            email=data.get('email'),
            telefone=telefone,
            estado=data.get('estado'),
            cidade=data.get('cidade'),
            servico_interesse=data.get('servico_interesse') or data.get('servico'),
            origem=data.get('origem', 'popup')
        )
        
        logger.info(f'Lead capturado: {lead.nome_completo} - {lead.telefone}')
        
        # Envia mensagem automática via WhatsApp
        whatsapp_result = whatsapp_service.send_welcome_message(
            phone=lead.telefone,
            name=lead.nome_completo
        )
        
        if whatsapp_result.get('success'):
            logger.info(f'Mensagem WhatsApp enviada com sucesso para {lead.nome_completo}')
        else:
            logger.warning(f'Falha ao enviar WhatsApp para {lead.nome_completo}: {whatsapp_result.get("error")}')
        
        return JsonResponse({
            'success': True,
            'message': 'Lead capturado com sucesso!',
            'lead_id': lead.id,
            'whatsapp_sent': whatsapp_result.get('success', False)
        })
    
    except Exception as e:
        logger.error(f'Erro ao capturar lead: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Erro ao capturar lead: {str(e)}'
        }, status=400)


# ------------------ Área do Cliente ------------------


@login_required
def dashboard_cliente(request):
    """Painel do cliente: lista chamados do cliente autenticado."""
    # Garante que exista um perfil Cliente para o usuário autenticado.
    perfil, _created = Cliente.objects.get_or_create(user=request.user)
    if _created:
        messages.info(request, 'Perfil de cliente criado automaticamente.')
    chamados = perfil.chamados.all().order_by('-data_criacao')

    return render(request, 'client/dashboard_cliente.html', {
        'perfil': perfil,
        'chamados': chamados,
    })


@login_required
def abrir_chamado(request):
    """View para abrir novo chamado pelo cliente autenticado."""
    # Cria o perfil Cliente se não existir, evitando erro para usuários que ainda não tenham sido vinculados.
    perfil, _created = Cliente.objects.get_or_create(user=request.user)
    if _created:
        messages.info(request, 'Perfil de cliente criado automaticamente.')

    if request.method == 'POST':
        form = ChamadoForm(request.POST, request.FILES)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.cliente = perfil
            chamado.save()

            # salvar anexos enviados na criação do chamado
            anexos = request.FILES.getlist('anexos')
            from .models import ChamadoAttachment
            for f in anexos:
                ChamadoAttachment.objects.create(chamado=chamado, arquivo=f, uploaded_by=request.user)

            messages.success(request, 'Chamado criado com sucesso.')
            return redirect('support:dashboard_cliente')
    else:
        form = ChamadoForm()

    return render(request, 'client/abrir_chamado.html', {'form': form})


@login_required
def chamado_detail(request, pk):
    """Exibe um chamado (thread de mensagens) e permite resposta do cliente."""
    chamado = get_object_or_404(Chamado, pk=pk)

    # Permitir apenas dono do chamado ou staff
    if not (request.user.is_staff or chamado.cliente.user == request.user):
        return JsonResponse({'success': False, 'error': 'Acesso negado.'}, status=403)

    form = ChamadoMessageForm()
    mensagens = chamado.mensagens.all().order_by('criado_em')

    return render(request, 'client/chamado_detail.html', {
        'chamado': chamado,
        'mensagens': mensagens,
        'form': form,
    })


@login_required
def responder_chamado(request, pk):
    """Permite que o cliente responda um chamado com texto e anexo opcional."""
    chamado = get_object_or_404(Chamado, pk=pk)
    # somente dono ou staff
    if not (request.user.is_staff or chamado.cliente.user == request.user):
        return JsonResponse({'success': False, 'error': 'Acesso negado.'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método inválido.'}, status=405)

    form = ChamadoMessageForm(request.POST, request.FILES)
    if form.is_valid():
        mensagem_text = form.cleaned_data['mensagem']
        anexo = form.cleaned_data.get('anexo')
        msg = ChamadoMessage.objects.create(
            chamado=chamado,
            autor=request.user,
            mensagem=mensagem_text,
            anexo=anexo if anexo else None
        )
        messages.success(request, 'Resposta enviada com sucesso.')
        return redirect('support:chamado_detail', pk=chamado.pk)

    mensagens = chamado.mensagens.all().order_by('criado_em')
    return render(request, 'client/chamado_detail.html', {'chamado': chamado, 'mensagens': mensagens, 'form': form})


# ==================== CHAMADOS API (STAFF) ====================

@login_required
@user_passes_test(is_staff_user)
def api_chamados_list(request):
    """Lista todos os chamados para o dashboard staff"""
    from django.utils import timezone
    chamados = Chamado.objects.all().select_related('cliente__user').prefetch_related('mensagens').order_by('-data_criacao')
    data = []
    for chamado in chamados:
        data.append({
            'id': chamado.id,
            'protocolo': f"#{chamado.id:05d}",
            'titulo': chamado.titulo,
            'cliente': chamado.cliente.user.get_full_name() or chamado.cliente.user.username,
            'cliente_email': chamado.cliente.user.email,
            'status': chamado.get_status_display(),
            'status_value': chamado.status,
            'prioridade': chamado.get_prioridade_display(),
            'prioridade_value': chamado.prioridade,
            'mensagens_count': chamado.mensagens.count(),
            'data_criacao': chamado.data_criacao.strftime('%d/%m/%Y %H:%M'),
            'data_atualizacao': chamado.data_atualizacao.strftime('%d/%m/%Y %H:%M')
        })
    return JsonResponse({'success': True, 'data': data})


@login_required
@user_passes_test(is_staff_user)
def api_chamado_detail(request, pk):
    """Retorna detalhes de um chamado específico incluindo mensagens"""
    chamado = get_object_or_404(Chamado, pk=pk)
    mensagens = chamado.mensagens.all().order_by('criado_em')
    
    mensagens_data = []
    for msg in mensagens:
        mensagens_data.append({
            'id': msg.id,
            'autor': msg.autor.get_full_name() or msg.autor.username,
            'autor_is_staff': msg.autor.is_staff,
            'mensagem': msg.mensagem,
            'anexo_url': msg.anexo.url if msg.anexo else None,
            'criado_em': msg.criado_em.strftime('%d/%m/%Y %H:%M')
        })
    
    data = {
        'id': chamado.id,
        'protocolo': f"#{chamado.id:05d}",
        'titulo': chamado.titulo,
        'descricao': chamado.descricao,
        'cliente': chamado.cliente.user.get_full_name() or chamado.cliente.user.username,
        'cliente_email': chamado.cliente.user.email,
        'status': chamado.get_status_display(),
        'status_value': chamado.status,
        'prioridade': chamado.get_prioridade_display(),
        'prioridade_value': chamado.prioridade,
        'data_criacao': chamado.data_criacao.strftime('%d/%m/%Y %H:%M'),
        'data_atualizacao': chamado.data_atualizacao.strftime('%d/%m/%Y %H:%M'),
        'mensagens': mensagens_data
    }
    
    return JsonResponse({'success': True, 'data': data})


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_chamado_respond(request, pk):
    """Permite que o staff responda um chamado"""
    from django.utils import timezone
    chamado = get_object_or_404(Chamado, pk=pk)
    
    try:
        data = json.loads(request.body)
        mensagem_text = data.get('mensagem', '').strip()
        
        if not mensagem_text:
            return JsonResponse({'success': False, 'error': 'Mensagem não pode estar vazia.'}, status=400)
        
        # Criar mensagem de resposta
        msg = ChamadoMessage.objects.create(
            chamado=chamado,
            autor=request.user,
            mensagem=mensagem_text
        )
        
        # Atualizar timestamp do chamado
        chamado.data_atualizacao = timezone.now()
        chamado.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Resposta enviada com sucesso!',
            'data': {
                'id': msg.id,
                'autor': msg.autor.get_full_name() or msg.autor.username,
                'mensagem': msg.mensagem,
                'criado_em': msg.criado_em.strftime('%d/%m/%Y %H:%M')
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_chamado_update_status(request, pk):
    """Atualiza o status de um chamado"""
    from django.utils import timezone
    chamado = get_object_or_404(Chamado, pk=pk)
    
    try:
        data = json.loads(request.body)
        novo_status = data.get('status')
        
        if novo_status not in dict(Chamado.STATUS_CHOICES).keys():
            return JsonResponse({'success': False, 'error': 'Status inválido.'}, status=400)
        
        chamado.status = novo_status
        chamado.data_atualizacao = timezone.now()
        chamado.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Status atualizado com sucesso!',
            'status_display': chamado.get_status_display()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ==================== NOTAS FISCAIS API (STAFF) ====================

@login_required
@user_passes_test(is_staff_user)
def api_clientes_list(request):
    """Lista todos os clientes para seleção no envio de NF"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    clientes = User.objects.filter(is_staff=False, is_active=True).order_by('first_name', 'username')
    data = []
    for cliente in clientes:
        data.append({
            'id': cliente.id,
            'nome': cliente.get_full_name() or cliente.username,
            'email': cliente.email,
            'username': cliente.username
        })
    return JsonResponse({'success': True, 'data': data})


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_nota_fiscal_enviar(request):
    """Envia uma nota fiscal para um cliente"""
    from apps.documents.models import NotaFiscal
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        cliente_id = request.POST.get('cliente_id')
        arquivo = request.FILES.get('arquivo')
        observacoes = request.POST.get('observacoes', '')
        
        if not cliente_id or not arquivo:
            return JsonResponse({'success': False, 'error': 'Cliente e arquivo são obrigatórios.'}, status=400)
        
        cliente = get_object_or_404(User, pk=cliente_id, is_staff=False)
        
        # Validar tipo de arquivo
        valid_extensions = ['.pdf', '.xml', '.zip']
        file_ext = arquivo.name[arquivo.name.rfind('.'):].lower()
        if file_ext not in valid_extensions:
            return JsonResponse({'success': False, 'error': 'Tipo de arquivo inválido. Use PDF, XML ou ZIP.'}, status=400)
        
        # Criar nota fiscal
        nota_fiscal = NotaFiscal.objects.create(
            cliente=cliente,
            enviado_por=request.user,
            arquivo_pdf=arquivo,
            observacoes=observacoes
        )
        
        logger.info(f"Nota fiscal enviada para {cliente.get_full_name()} por {request.user.get_full_name()}")
        
        return JsonResponse({
            'success': True,
            'message': f'Nota fiscal enviada com sucesso para {cliente.get_full_name() or cliente.username}!',
            'data': {
                'id': nota_fiscal.id,
                'cliente': cliente.get_full_name() or cliente.username,
                'arquivo': nota_fiscal.nome_arquivo,
                'data_envio': nota_fiscal.data_upload.strftime('%d/%m/%Y %H:%M')
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao enviar nota fiscal: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@user_passes_test(is_staff_user)
def api_notas_fiscais_list(request):
    """Lista todas as notas fiscais enviadas"""
    from apps.documents.models import NotaFiscal
    
    notas = NotaFiscal.objects.all().select_related('cliente', 'enviado_por').order_by('-data_upload')
    data = []
    for nota in notas:
        data.append({
            'id': nota.id,
            'cliente': nota.cliente.get_full_name() or nota.cliente.username,
            'cliente_email': nota.cliente.email,
            'arquivo': nota.nome_arquivo,
            'observacoes': nota.observacoes or '',
            'enviado_por': nota.enviado_por.get_full_name() if nota.enviado_por else 'Sistema',
            'data_upload': nota.data_upload.strftime('%d/%m/%Y %H:%M')
        })
    return JsonResponse({'success': True, 'data': data})


@login_required
@user_passes_test(is_staff_user)
def api_contabilidade_clientes(request):
    """Lista clientes que possuem movimentações financeiras"""
    from apps.users.models import MovimentacaoFinanceira
    from django.contrib.auth import get_user_model
    from django.db.models import Count
    
    User = get_user_model()
    
    # Buscar clientes com movimentações
    clientes_com_mov = User.objects.filter(
        movimentacoes__isnull=False
    ).annotate(
        total_movimentacoes=Count('movimentacoes')
    ).distinct().order_by('first_name', 'last_name')
    
    data = []
    for cliente in clientes_com_mov:
        data.append({
            'id': cliente.id,
            'nome': cliente.get_full_name() or cliente.username,
            'email': cliente.email,
            'cpf_cnpj': cliente.cpf_cnpj or 'Não informado',
            'total_movimentacoes': cliente.total_movimentacoes
        })
    
    return JsonResponse({'success': True, 'data': data})


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_certidao_enviar(request):
    """Envia uma certidão negativa para um cliente"""
    from apps.users.models import CertidaoNegativa
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        cliente_id = request.POST.get('cliente_id')
        tipo_certidao = request.POST.get('tipo_certidao')
        arquivo = request.FILES.get('arquivo')
        status_certidao = request.POST.get('status', 'negativa')
        
        if not cliente_id or not tipo_certidao or not arquivo:
            return JsonResponse({'success': False, 'error': 'Cliente, tipo e arquivo são obrigatórios.'}, status=400)
        
        cliente = get_object_or_404(User, pk=cliente_id, is_staff=False)
        
        # Validar tipo de arquivo
        valid_extensions = ['.pdf', '.zip']
        file_ext = arquivo.name[arquivo.name.rfind('.'):].lower()
        if file_ext not in valid_extensions:
            return JsonResponse({'success': False, 'error': 'Tipo de arquivo inválido. Use PDF ou ZIP.'}, status=400)
        
        # Validar tipo de certidão
        tipos_validos = ['federal', 'estadual', 'trabalhista', 'fgts']
        if tipo_certidao not in tipos_validos:
            return JsonResponse({'success': False, 'error': 'Tipo de certidão inválido.'}, status=400)
        
        # Criar certidão
        certidao = CertidaoNegativa.objects.create(
            cliente=cliente,
            tipo=tipo_certidao,
            status=status_certidao,
            arquivo_pdf=arquivo
        )
        
        logger.info(f"Certidão {tipo_certidao} enviada para {cliente.get_full_name()} por {request.user.get_full_name()}")
        
        return JsonResponse({
            'success': True,
            'message': f'Certidão {certidao.get_tipo_display()} enviada com sucesso para {cliente.get_full_name() or cliente.username}!',
            'data': {
                'id': certidao.id,
                'tipo': certidao.get_tipo_display(),
                'cliente': cliente.get_full_name() or cliente.username,
                'data_envio': certidao.data_envio.strftime('%d/%m/%Y %H:%M')
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao enviar certidão: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@user_passes_test(is_staff_user)
def api_certidoes_list(request):
    """Lista todas as certidões negativas enviadas"""
    from apps.users.models import CertidaoNegativa
    
    certidoes = CertidaoNegativa.objects.all().select_related('cliente').order_by('-data_envio')
    data = []
    for cert in certidoes:
        data.append({
            'id': cert.id,
            'cliente': cert.cliente.get_full_name() or cert.cliente.username,
            'cliente_email': cert.cliente.email,
            'tipo': cert.get_tipo_display(),
            'tipo_raw': cert.tipo,
            'status': cert.get_status_display(),
            'status_raw': cert.status,
            'arquivo_url': cert.arquivo_pdf.url if cert.arquivo_pdf else None,
            'data_envio': cert.data_envio.strftime('%d/%m/%Y %H:%M')
        })
    return JsonResponse({'success': True, 'data': data})


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_documento_empresa_enviar(request):
    """Envia um documento da empresa para um cliente"""
    from apps.documents.models import DocumentoEmpresa
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        cliente_id = request.POST.get('cliente_id')
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        arquivo = request.FILES.get('arquivo')
        descricao = request.POST.get('descricao', '')
        
        if not cliente_id or not titulo or not categoria or not arquivo:
            return JsonResponse({'success': False, 'error': 'Cliente, título, categoria e arquivo são obrigatórios.'}, status=400)
        
        cliente = get_object_or_404(User, pk=cliente_id, is_staff=False)
        
        # Validar categoria
        categorias_validas = ['contrato_social', 'alvara', 'certidao', 'procuracao', 'registro', 'declaracao', 'relatorio', 'outros']
        if categoria not in categorias_validas:
            return JsonResponse({'success': False, 'error': 'Categoria inválida.'}, status=400)
        
        # Criar documento
        documento = DocumentoEmpresa.objects.create(
            cliente=cliente,
            titulo=titulo,
            categoria=categoria,
            arquivo=arquivo,
            descricao=descricao
        )
        
        logger.info(f"Documento '{titulo}' enviado para {cliente.get_full_name()} por {request.user.get_full_name()}")
        
        return JsonResponse({
            'success': True,
            'message': f'Documento "{titulo}" enviado com sucesso para {cliente.get_full_name() or cliente.username}!',
            'data': {
                'id': documento.id,
                'titulo': documento.titulo,
                'categoria': documento.get_categoria_display(),
                'cliente': cliente.get_full_name() or cliente.username,
                'data_upload': documento.data_upload.strftime('%d/%m/%Y %H:%M')
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao enviar documento: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@user_passes_test(is_staff_user)
def api_documentos_empresa_list(request):
    """Lista todos os documentos da empresa enviados"""
    from apps.documents.models import DocumentoEmpresa
    
    documentos = DocumentoEmpresa.objects.all().select_related('cliente').order_by('-data_upload')
    data = []
    for doc in documentos:
        data.append({
            'id': doc.id,
            'cliente': doc.cliente.get_full_name() or doc.cliente.username,
            'cliente_email': doc.cliente.email,
            'titulo': doc.titulo,
            'categoria': doc.get_categoria_display(),
            'categoria_raw': doc.categoria,
            'descricao': doc.descricao or '',
            'arquivo_url': doc.arquivo.url if doc.arquivo else None,
            'nome_arquivo': doc.nome_arquivo,
            'tamanho': doc.tamanho_arquivo,
            'data_upload': doc.data_upload.strftime('%d/%m/%Y %H:%M')
        })
    return JsonResponse({'success': True, 'data': data})


@login_required
@user_passes_test(is_staff_user)
def api_extratos_bancarios_cliente(request, cliente_id):
    """Lista todos os extratos bancários de um cliente específico"""
    from apps.documents.models import ExtratoBancario
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    cliente = get_object_or_404(User, pk=cliente_id)
    
    # Buscar todos os extratos do cliente
    extratos = ExtratoBancario.objects.filter(cliente=cliente).order_by('-data_upload')
    
    data = []
    for extrato in extratos:
        # Calcular tamanho do arquivo
        try:
            tamanho_bytes = extrato.arquivo.size
            if tamanho_bytes < 1024:
                tamanho = f"{tamanho_bytes} B"
            elif tamanho_bytes < 1024 * 1024:
                tamanho = f"{tamanho_bytes / 1024:.1f} KB"
            else:
                tamanho = f"{tamanho_bytes / (1024 * 1024):.1f} MB"
        except:
            tamanho = "N/A"
        
        # Obter nome do arquivo
        try:
            nome_arquivo = extrato.arquivo.name.split('/')[-1]
        except:
            nome_arquivo = "Arquivo"
        
        # Obter extensão
        try:
            extensao = nome_arquivo.split('.')[-1].upper() if '.' in nome_arquivo else 'Arquivo'
        except:
            extensao = 'Arquivo'
        
        data.append({
            'id': extrato.id,
            'mes_ano': extrato.mes_ano,
            'start_date': extrato.start_date.strftime('%d/%m/%Y') if extrato.start_date else None,
            'end_date': extrato.end_date.strftime('%d/%m/%Y') if extrato.end_date else None,
            'observacoes': extrato.observacoes or '',
            'arquivo_url': extrato.arquivo.url if extrato.arquivo else None,
            'nome_arquivo': nome_arquivo,
            'extensao': extensao,
            'tamanho': tamanho,
            'data_upload': extrato.data_upload.strftime('%d/%m/%Y %H:%M')
        })
    
    return JsonResponse({
        'success': True,
        'cliente': {
            'id': cliente.id,
            'nome': cliente.get_full_name() or cliente.username,
            'email': cliente.email
        },
        'data': data
    })


@login_required
@user_passes_test(is_staff_user)
def api_clientes_com_extratos(request):
    """Lista clientes que possuem extratos bancários"""
    from apps.documents.models import ExtratoBancario
    from django.contrib.auth import get_user_model
    from django.db.models import Count
    
    User = get_user_model()
    
    # Buscar clientes com extratos
    clientes_com_extratos = User.objects.filter(
        extratos_bancarios__isnull=False
    ).annotate(
        total_extratos=Count('extratos_bancarios')
    ).distinct().order_by('first_name', 'last_name')
    
    data = []
    for cliente in clientes_com_extratos:
        data.append({
            'id': cliente.id,
            'nome': cliente.get_full_name() or cliente.username,
            'email': cliente.email,
            'total_extratos': cliente.total_extratos
        })
    
    return JsonResponse({'success': True, 'data': data})


@login_required
@user_passes_test(is_staff_user)
def api_contabilidade_movimentacoes(request, cliente_id):
    """Lista movimentações financeiras de um cliente específico, agrupadas por mês"""
    from apps.users.models import MovimentacaoFinanceira
    from django.contrib.auth import get_user_model
    from collections import defaultdict
    from datetime import datetime
    
    User = get_user_model()
    
    cliente = get_object_or_404(User, pk=cliente_id)
    
    # Buscar todas as movimentações do cliente
    movimentacoes = MovimentacaoFinanceira.objects.filter(
        user=cliente
    ).order_by('-competencia', '-created_at')
    
    # Agrupar por mês/ano
    movimentacoes_por_mes = defaultdict(list)
    
    for mov in movimentacoes:
        mes_ano = mov.competencia.strftime('%Y-%m')
        mes_ano_formatado = mov.competencia.strftime('%B de %Y')
        
        # Traduzir mês para português
        meses_pt = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }
        
        for eng, pt in meses_pt.items():
            mes_ano_formatado = mes_ano_formatado.replace(eng, pt)
        
        movimentacoes_por_mes[mes_ano].append({
            'id': mov.id,
            'tipo': mov.get_tipo_display(),
            'tipo_raw': mov.tipo,
            'nome': mov.nome,
            'valor': float(mov.valor),
            'valor_formatado': f'R$ {mov.valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
            'status': mov.get_status_display(),
            'status_raw': mov.status,
            'anexo_url': mov.anexo.url if mov.anexo else None,
            'data_criacao': mov.created_at.strftime('%d/%m/%Y %H:%M'),
            'mes_ano_formatado': mes_ano_formatado
        })
    
    # Converter para lista ordenada
    data = []
    for mes_ano in sorted(movimentacoes_por_mes.keys(), reverse=True):
        movs = movimentacoes_por_mes[mes_ano]
        
        # Calcular totais
        total_receitas = sum(m['valor'] for m in movs if m['tipo_raw'] == 'receita')
        total_despesas = sum(m['valor'] for m in movs if m['tipo_raw'] == 'despesa')
        saldo = total_receitas - total_despesas
        
        data.append({
            'mes_ano': mes_ano,
            'mes_ano_formatado': movs[0]['mes_ano_formatado'],
            'movimentacoes': movs,
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'saldo': saldo,
            'total_receitas_formatado': f'R$ {total_receitas:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
            'total_despesas_formatado': f'R$ {total_despesas:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
            'saldo_formatado': f'R$ {saldo:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        })
    
    return JsonResponse({
        'success': True,
        'cliente': {
            'id': cliente.id,
            'nome': cliente.get_full_name() or cliente.username,
            'email': cliente.email,
            'cpf_cnpj': cliente.cpf_cnpj or 'Não informado'
        },
        'data': data
    })


@login_required
@user_passes_test(is_staff_user)
def api_clientes_fase_list(request):
    """Lista clientes e suas fases de abertura"""
    from apps.support.models import Cliente
    
    clientes = Cliente.objects.select_related('user').all().order_by('user__first_name')
    data = []
    
    for cliente in clientes:
        data.append({
            'id': cliente.id,
            'user_id': cliente.user.id,
            'nome': cliente.user.get_full_name() or cliente.user.username,
            'email': cliente.user.email,
            'fase_abertura': cliente.fase_abertura,
            'fase_abertura_display': cliente.get_fase_abertura_display()
        })
        
    return JsonResponse({'success': True, 'data': data})


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def api_cliente_fase_update(request):
    """Atualiza a fase de abertura de um cliente"""
    from apps.support.models import Cliente
    
    try:
        data = json.loads(request.body)
        cliente_id = data.get('cliente_id')
        fase = data.get('fase')
        
        if not cliente_id or not fase:
            return JsonResponse({'success': False, 'error': 'Cliente ID e Fase são obrigatórios'}, status=400)
            
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.fase_abertura = fase
        cliente.save()
        
        return JsonResponse({
            'success': True, 
            'message': f'Fase atualizada para {cliente.get_fase_abertura_display()}',
            'fase_display': cliente.get_fase_abertura_display()
        })
        
    except Exception as e:
        logger.error(f"Erro ao atualizar fase do cliente: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
