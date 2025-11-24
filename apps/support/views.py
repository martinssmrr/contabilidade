from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers import serialize
from django.forms.models import model_to_dict
import json
import logging
from .models import Lead, Ticket
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
    Dashboard administrativa para gerenciamento de leads e outros recursos.
    """
    return render(request, 'staff/dashboard.html')

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
        lead.contatado = data.get('contatado', lead.contatado)
        lead.observacoes = data.get('observacoes', lead.observacoes)
        
        lead.save()
        return JsonResponse({'success': True})
    except Exception as e:
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
    """
    try:
        data = json.loads(request.body)
        
        # Cria o lead no banco de dados
        lead = Lead.objects.create(
            nome_completo=data.get('nome_completo'),
            email=data.get('email'),
            telefone=data.get('telefone'),
            estado=data.get('estado'),
            cidade=data.get('cidade'),
            servico_interesse=data.get('servico'),
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
