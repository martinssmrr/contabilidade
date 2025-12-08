import json
import logging
import mercadopago
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from apps.services.models import Plano
from .models import Pagamento

logger = logging.getLogger(__name__)


def checkout_plano(request, plano_id):
    """
    Página de checkout para um plano específico.
    Renderiza o Checkout Bricks do Mercado Pago.
    """
    plano = get_object_or_404(Plano, id=plano_id, ativo=True)
    
    # Criar registro de pagamento pendente
    pagamento = Pagamento.objects.create(
        plano=plano,
        valor=plano.preco,
        status='pendente',
        cliente=request.user if request.user.is_authenticated else None,
    )
    
    # Configurar SDK do Mercado Pago
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    
    # URLs de callback
    site_url = settings.SITE_URL.rstrip('/')
    
    # Criar preferência de pagamento (simplificada para funcionar em localhost)
    preference_data = {
        "items": [
            {
                "id": str(plano.id),
                "title": f"Plano {plano.nome} - Vetorial Contabilidade",
                "description": plano.descricao[:255] if plano.descricao else f"Plano de contabilidade {plano.nome}",
                "category_id": "services",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(plano.preco)
            }
        ],
        "external_reference": str(pagamento.external_reference),
        "statement_descriptor": "VETORIAL",
    }
    
    # Adicionar payer apenas se tiver dados
    if request.user.is_authenticated and request.user.email:
        preference_data["payer"] = {
            "name": request.user.first_name or "Cliente",
            "email": request.user.email,
        }
    
    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})
        
        if preference.get("id"):
            # Salvar ID da preferência
            pagamento.mp_preference_id = preference["id"]
            pagamento.save()
            
            logger.info(f"Preferência criada: {preference['id']} para pagamento {pagamento.id}")
        else:
            logger.error(f"Erro ao criar preferência: {preference_response}")
            
    except Exception as e:
        logger.error(f"Erro ao criar preferência MP: {e}")
        preference = {}
    
    context = {
        'plano': plano,
        'pagamento': pagamento,
        'preference_id': preference.get("id", ""),
        'mp_public_key': settings.MERCADO_PAGO_PUBLIC_KEY,
        'site_url': site_url,
    }
    
    return render(request, 'payments/checkout.html', context)


@require_POST
@csrf_exempt
def processar_pagamento(request):
    """
    Processa o pagamento via Checkout Bricks (Payment Brick).
    Recebe os dados do formulário de pagamento do frontend.
    """
    try:
        data = json.loads(request.body)
        logger.info(f"Dados recebidos do frontend: {data}")
        
        external_reference = data.get('external_reference')
        payment_data = data.get('payment_data', {})
        form_data = payment_data.get('formData', {})
        
        if not external_reference:
            return JsonResponse({'error': 'Referência externa não encontrada', 'status': 400}, status=400)
        
        pagamento = get_object_or_404(Pagamento, external_reference=external_reference)
        
        # Configurar SDK
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        
        # Extrair dados do Payment Brick
        # O Payment Brick envia os dados em formData
        token = form_data.get('token') or payment_data.get('token')
        installments = form_data.get('installments') or payment_data.get('installments', 1)
        payment_method_id = form_data.get('payment_method_id') or payment_data.get('payment_method_id')
        issuer_id = form_data.get('issuer_id') or payment_data.get('issuer_id')
        payer_data = form_data.get('payer', {}) or payment_data.get('payer', {})
        
        # Criar pagamento no Mercado Pago
        payment_create_data = {
            "transaction_amount": float(pagamento.valor),
            "token": token,
            "description": f"Plano {pagamento.plano.nome} - Vetorial Contabilidade" if pagamento.plano else "Serviço Vetorial",
            "installments": int(installments) if installments else 1,
            "payment_method_id": payment_method_id,
            "payer": {
                "email": payer_data.get("email", "test@test.com"),
            },
            "external_reference": str(external_reference),
        }
        
        # Adicionar issuer_id se existir
        if issuer_id:
            payment_create_data["issuer_id"] = issuer_id
        
        # Adicionar identification se existir
        if payer_data.get("identification"):
            payment_create_data["payer"]["identification"] = payer_data["identification"]
        
        logger.info(f"Enviando para MP: {payment_create_data}")
        
        payment_response = sdk.payment().create(payment_create_data)
        payment_result = payment_response.get("response", {})
        
        logger.info(f"Resposta do MP: {payment_response}")
        
        # Verificar se houve erro na resposta
        if payment_response.get("status") >= 400:
            error_msg = payment_result.get("message", "Erro desconhecido")
            logger.error(f"Erro do MP: {payment_response}")
            return JsonResponse({
                'status': 'error',
                'status_detail': error_msg,
                'payment_id': None,
                'redirect_url': None,
                'error': payment_result
            })
        
        # Atualizar pagamento local
        pagamento.mp_payment_id = str(payment_result.get("id", ""))
        pagamento.mp_status = payment_result.get("status", "")
        pagamento.mp_status_detail = payment_result.get("status_detail", "")
        pagamento.mp_payment_method_id = payment_result.get("payment_method_id", "")
        pagamento.mp_payment_type_id = payment_result.get("payment_type_id", "")
        pagamento.mp_response_data = payment_result
        
        # Atualizar dados do cliente
        payer_info = payment_result.get("payer", {})
        if payer_info:
            pagamento.cliente_email = payer_info.get("email", "")
            pagamento.cliente_nome = f"{payer_info.get('first_name', '')} {payer_info.get('last_name', '')}".strip()
            identification = payer_info.get("identification", {})
            if identification.get("type") == "CPF":
                pagamento.cliente_cpf = identification.get("number", "")
        
        # Mapear status do MP para status interno
        mp_status = payment_result.get("status", "")
        if mp_status == "approved":
            pagamento.status = "aprovado"
            pagamento.pago_em = timezone.now()
        elif mp_status in ["pending", "in_process", "authorized"]:
            pagamento.status = "processando"
        elif mp_status in ["rejected", "cancelled"]:
            pagamento.status = "rejeitado"
        else:
            pagamento.status = "erro"
        
        pagamento.save()
        
        logger.info(f"Pagamento {pagamento.id} processado: {mp_status}")
        
        return JsonResponse({
            'status': mp_status,
            'status_detail': payment_result.get("status_detail", ""),
            'payment_id': payment_result.get("id"),
            'redirect_url': reverse('payments:pagamento_sucesso') + f"?external_reference={external_reference}" if mp_status == "approved" else None,
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dados inválidos', 'status': 400}, status=400)
    except Exception as e:
        logger.error(f"Erro ao processar pagamento: {e}", exc_info=True)
        return JsonResponse({'error': str(e), 'status': 500}, status=500)


@csrf_exempt
@require_POST
def webhook_mercadopago(request):
    """
    Webhook para receber notificações do Mercado Pago.
    Atualiza o status dos pagamentos automaticamente.
    """
    try:
        # Obter dados da notificação
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        logger.info(f"Webhook MP recebido: {data}")
        
        notification_type = data.get('type') or data.get('topic')
        
        if notification_type == 'payment':
            payment_id = data.get('data', {}).get('id') or data.get('id')
            
            if payment_id:
                # Buscar detalhes do pagamento no MP
                sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
                payment_info = sdk.payment().get(payment_id)
                payment_data = payment_info.get("response", {})
                
                external_reference = payment_data.get("external_reference")
                
                if external_reference:
                    try:
                        pagamento = Pagamento.objects.get(external_reference=external_reference)
                        
                        # Atualizar dados
                        pagamento.mp_payment_id = str(payment_id)
                        pagamento.mp_status = payment_data.get("status", "")
                        pagamento.mp_status_detail = payment_data.get("status_detail", "")
                        pagamento.mp_payment_method_id = payment_data.get("payment_method_id", "")
                        pagamento.mp_payment_type_id = payment_data.get("payment_type_id", "")
                        pagamento.mp_response_data = payment_data
                        
                        # Mapear status
                        mp_status = payment_data.get("status", "")
                        if mp_status == "approved":
                            pagamento.status = "aprovado"
                            if not pagamento.pago_em:
                                pagamento.pago_em = timezone.now()
                        elif mp_status in ["pending", "in_process", "authorized"]:
                            pagamento.status = "processando"
                        elif mp_status == "refunded":
                            pagamento.status = "reembolsado"
                        elif mp_status in ["rejected", "cancelled"]:
                            pagamento.status = "rejeitado"
                        
                        pagamento.save()
                        logger.info(f"Pagamento {pagamento.id} atualizado via webhook: {mp_status}")
                        
                    except Pagamento.DoesNotExist:
                        logger.warning(f"Pagamento não encontrado para external_reference: {external_reference}")
        
        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Erro no webhook MP: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_GET
def pagamento_sucesso(request):
    """
    Página de sucesso após pagamento aprovado.
    """
    external_reference = request.GET.get('external_reference')
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    
    pagamento = None
    if external_reference:
        try:
            pagamento = Pagamento.objects.get(external_reference=external_reference)
            
            # Se recebemos payment_id do redirect, atualizar
            if payment_id and not pagamento.mp_payment_id:
                pagamento.mp_payment_id = payment_id
                pagamento.mp_status = status or 'approved'
                pagamento.status = 'aprovado'
                pagamento.pago_em = timezone.now()
                pagamento.save()
                
        except Pagamento.DoesNotExist:
            pass
    
    # Redirecionar para página de obrigado
    return redirect('obrigado')


@require_GET
def pagamento_erro(request):
    """
    Página de erro quando pagamento falha.
    """
    external_reference = request.GET.get('external_reference')
    
    pagamento = None
    if external_reference:
        try:
            pagamento = Pagamento.objects.get(external_reference=external_reference)
            pagamento.status = 'rejeitado'
            pagamento.save()
        except Pagamento.DoesNotExist:
            pass
    
    context = {
        'pagamento': pagamento,
        'mensagem': 'Houve um problema com seu pagamento. Por favor, tente novamente.',
    }
    
    return render(request, 'payments/erro.html', context)


@require_GET
def pagamento_pendente(request):
    """
    Página quando pagamento está pendente (boleto, por exemplo).
    """
    external_reference = request.GET.get('external_reference')
    
    pagamento = None
    if external_reference:
        try:
            pagamento = Pagamento.objects.get(external_reference=external_reference)
            pagamento.status = 'processando'
            pagamento.save()
        except Pagamento.DoesNotExist:
            pass
    
    context = {
        'pagamento': pagamento,
        'mensagem': 'Seu pagamento está sendo processado. Você receberá uma confirmação em breve.',
    }
    
    return render(request, 'payments/pendente.html', context)
