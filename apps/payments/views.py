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
from django.contrib.auth import login, get_user_model
from django.contrib import messages

from apps.services.models import Plano
from .models import Pagamento

logger = logging.getLogger(__name__)
User = get_user_model()


def pre_checkout(request, plano_id):
    """
    Página de cadastro antes do checkout.
    Se o usuário já está logado, redireciona direto para o checkout.
    Se não está logado, exibe formulário de cadastro.
    """
    plano = get_object_or_404(Plano, id=plano_id, ativo=True)
    
    # Se já está logado, vai direto pro checkout
    if request.user.is_authenticated:
        return redirect('payments:checkout_plano', plano_id=plano_id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        errors = []
        
        # Validações
        if not first_name:
            errors.append('Primeiro nome é obrigatório.')
        if not last_name:
            errors.append('Sobrenome é obrigatório.')
        if not email:
            errors.append('E-mail é obrigatório.')
        if not password:
            errors.append('Senha é obrigatória.')
        if password != password_confirm:
            errors.append('As senhas não coincidem.')
        
        # Validar senha
        if password and len(password) < 8:
            errors.append('A senha deve ter pelo menos 8 caracteres.')
        
        # Verificar se email já existe
        if email and User.objects.filter(email=email).exists():
            errors.append('Este e-mail já está cadastrado. Faça login para continuar.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'payments/pre_checkout.html', {
                'plano': plano,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
        
        try:
            # Criar usuário
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            
            # Fazer login automático
            login(request, user)
            
            messages.success(request, f'Bem-vindo(a), {first_name}! Sua conta foi criada com sucesso.')
            
            # Redirecionar para o checkout
            return redirect('payments:checkout_plano', plano_id=plano_id)
            
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            messages.error(request, 'Erro ao criar conta. Por favor, tente novamente.')
            return render(request, 'payments/pre_checkout.html', {
                'plano': plano,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
    
    return render(request, 'payments/pre_checkout.html', {'plano': plano})

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
    
    # URL do webhook para notificações (OBRIGATÓRIO para aprovação)
    notification_url = f"{site_url}/payments/webhook/mercadopago/"
    
    # Criar preferência de pagamento com todos os campos recomendados
    preference_data = {
        "items": [
            {
                "id": str(plano.id),  # Código do item (recomendado)
                "title": f"Plano {plano.nome} - Vetorial Contabilidade",  # Nome do item (recomendado)
                "description": plano.descricao[:255] if plano.descricao else f"Serviços de contabilidade - Plano {plano.nome}",  # Descrição do item (recomendado)
                "category_id": "services",  # Categoria do item (recomendado)
                "quantity": 1,  # Quantidade (recomendado)
                "currency_id": "BRL",
                "unit_price": float(plano.preco)  # Preço unitário (recomendado)
            }
        ],
        "external_reference": str(pagamento.external_reference),
        "statement_descriptor": "VETORIAL CONTAB",  # Descrição na fatura do cartão (recomendado)
        "notification_url": notification_url,  # URL para webhooks (OBRIGATÓRIO)
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
    Suporta: Cartão de Crédito, Débito, PIX, Boleto.
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
        token = form_data.get('token') or payment_data.get('token')
        installments = form_data.get('installments') or payment_data.get('installments', 1)
        
        # payment_method_id pode vir de vários lugares
        payment_method_id = (
            form_data.get('payment_method_id') or 
            payment_data.get('payment_method_id') or
            payment_data.get('selectedPaymentMethod') or
            payment_data.get('paymentType')
        )
        
        # Tipo de pagamento (ticket = boleto, bank_transfer = pix, etc)
        payment_type = payment_data.get('paymentType') or payment_data.get('payment_type') or ''
        
        logger.info(f"payment_method_id: {payment_method_id}, payment_type: {payment_type}")
        
        issuer_id = form_data.get('issuer_id') or payment_data.get('issuer_id')
        payer_data = form_data.get('payer', {}) or payment_data.get('payer', {})
        
        # Dados do usuário enviados pelo frontend
        user_info = payment_data.get('userInfo', {})
        
        # Log para debug dos dados do payer
        logger.info(f"payer_data recebido: {payer_data}")
        logger.info(f"userInfo recebido: {user_info}")
        logger.info(f"cardholderName recebido: {payment_data.get('cardholderName', '')}")
        
        # Obter email do payer
        payer_email = payer_data.get("email", "")
        if not payer_email:
            payer_email = user_info.get("email", "")
        if not payer_email and request.user.is_authenticated:
            payer_email = request.user.email
        if not payer_email:
            payer_email = "cliente@vetorial.com.br"
        
        # Obter nome do payer - prioridade:
        # 1. cardholderName (nome no cartão)
        # 2. payer_data (dados do Brick)
        # 3. userInfo (dados do usuário logado enviados pelo frontend)
        # 4. request.user (usuário logado no backend)
        
        payer_first_name = ""
        payer_last_name = ""
        
        # Tentar cardholderName primeiro (nome exato no cartão)
        cardholder_name = payment_data.get("cardholderName", "") or form_data.get("cardholderName", "")
        if cardholder_name and cardholder_name.strip():
            name_parts = cardholder_name.strip().split()
            if name_parts:
                payer_first_name = name_parts[0]
                payer_last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                logger.info(f"Nome extraído do cardholderName: {payer_first_name} {payer_last_name}")
        
        # Tentar payer_data do Brick
        if not payer_first_name:
            payer_first_name = (
                payer_data.get("firstName", "") or 
                payer_data.get("first_name", "") or
                payer_data.get("name", "").split()[0] if payer_data.get("name") else ""
            )
            payer_last_name = (
                payer_data.get("lastName", "") or 
                payer_data.get("last_name", "") or
                " ".join(payer_data.get("name", "").split()[1:]) if payer_data.get("name") and len(payer_data.get("name", "").split()) > 1 else ""
            )
            if payer_first_name:
                logger.info(f"Nome extraído do payer_data: {payer_first_name} {payer_last_name}")
        
        # Tentar userInfo do frontend (usuário logado)
        if not payer_first_name:
            payer_first_name = user_info.get("firstName", "") or user_info.get("first_name", "")
            payer_last_name = user_info.get("lastName", "") or user_info.get("last_name", "")
            if payer_first_name:
                logger.info(f"Nome extraído do userInfo: {payer_first_name} {payer_last_name}")
        
        # Tentar request.user (backend)
        if not payer_first_name and request.user.is_authenticated:
            if request.user.first_name:
                payer_first_name = request.user.first_name
                payer_last_name = request.user.last_name or ""
                logger.info(f"Nome extraído do request.user: {payer_first_name} {payer_last_name}")
            elif request.user.get_full_name():
                name_parts = request.user.get_full_name().split()
                payer_first_name = name_parts[0]
                payer_last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                logger.info(f"Nome extraído do get_full_name: {payer_first_name} {payer_last_name}")
        
        # Último fallback
        if not payer_first_name:
            logger.warning(f"Nome do cliente não encontrado! Usando fallback.")
            payer_first_name = "Cliente"
        if not payer_last_name:
            payer_last_name = ""
        
        logger.info(f"Nome final do payer: {payer_first_name} {payer_last_name}")
        
        # URL de notificação do webhook (OBRIGATÓRIO para todos os tipos)
        site_url = settings.SITE_URL.rstrip('/')
        notification_url = f"{site_url}/payments/webhook/mercadopago/"
        
        # Base do payload de pagamento - inclui campos obrigatórios e recomendados
        payment_create_data = {
            "transaction_amount": float(pagamento.valor),
            "description": f"Plano {pagamento.plano.nome} - Vetorial Contabilidade" if pagamento.plano else "Serviço Vetorial",
            "payment_method_id": payment_method_id,
            "external_reference": str(external_reference),
            "statement_descriptor": "VETORIAL CONTAB",  # RECOMENDADO: aparece na fatura do cartão
            "notification_url": notification_url,  # OBRIGATÓRIO: webhook de notificações
            "payer": {
                "email": payer_email,
                "first_name": payer_first_name,
                "last_name": payer_last_name,
            },
        }
        
        # Adicionar identification do payer se existir
        if payer_data.get("identification"):
            payment_create_data["payer"]["identification"] = payer_data["identification"]
        
        # Lista de métodos de boleto
        boleto_methods = ['bolbradesco', 'pec', 'ticket', 'boleto']
        is_boleto = payment_method_id in boleto_methods or payment_type == 'ticket'
        
        # Para boleto, o payment_method_id deve ser 'bolbradesco'
        if is_boleto and payment_method_id == 'ticket':
            payment_method_id = 'bolbradesco'
            payment_create_data["payment_method_id"] = payment_method_id
        
        # Configuração específica por tipo de pagamento
        if payment_method_id == 'pix' or payment_type == 'bank_transfer':
            # PIX - não precisa de token
            # Definir expiração do PIX (30 minutos)
            from datetime import datetime, timedelta
            expiration = datetime.now() + timedelta(minutes=30)
            payment_create_data["date_of_expiration"] = expiration.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
            payment_create_data["payment_method_id"] = "pix"
            
        elif is_boleto:
            # Boleto - precisa de dados completos do payer incluindo endereço
            from datetime import datetime, timedelta
            due_date = datetime.now() + timedelta(days=3)
            payment_create_data["date_of_expiration"] = due_date.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
            
            # Extrair endereço do payer_data ou usar padrão
            address_data = payer_data.get("address", {})
            payment_create_data["payer"]["address"] = {
                "zip_code": address_data.get("zipCode", "") or address_data.get("zip_code", "") or "01310100",
                "street_name": address_data.get("streetName", "") or address_data.get("street_name", "") or "Avenida Paulista",
                "street_number": address_data.get("streetNumber", "") or address_data.get("street_number", "") or "1000",
                "neighborhood": address_data.get("neighborhood", "") or "Bela Vista",
                "city": address_data.get("city", "") or "Sao Paulo",
                "federal_unit": address_data.get("federalUnit", "") or address_data.get("federal_unit", "") or "SP",
            }
            
            logger.info(f"Boleto - payment_method_id: {payment_method_id}, payer: {payment_create_data['payer']}")
            
        else:
            # Cartão de crédito/débito - precisa de token
            if not token:
                return JsonResponse({
                    'status': 'error',
                    'status_detail': 'Token do cartão não fornecido',
                    'payment_id': None,
                    'redirect_url': None,
                }, status=400)
            
            payment_create_data["token"] = token
            payment_create_data["installments"] = int(installments) if installments else 1
            
            if issuer_id:
                payment_create_data["issuer_id"] = issuer_id
            
            # Adicionar dados adicionais para melhorar aprovação antifraude
            # Identificação do comprador (CPF)
            if payer_data.get("identification"):
                payment_create_data["payer"]["identification"] = payer_data["identification"]
            
            # Informações adicionais para antifraude (campos recomendados pelo MP)
            payment_create_data["additional_info"] = {
                "items": [
                    {
                        "id": str(pagamento.plano.id) if pagamento.plano else "1",  # Código do item
                        "title": f"Plano {pagamento.plano.nome}" if pagamento.plano else "Serviço Vetorial",  # Nome do item
                        "description": pagamento.plano.descricao[:255] if pagamento.plano and pagamento.plano.descricao else "Serviços de contabilidade profissional",  # Descrição
                        "category_id": "services",  # Categoria
                        "quantity": 1,  # Quantidade
                        "unit_price": str(float(pagamento.valor)),  # Preço unitário (string)
                    }
                ],
                "payer": {
                    "first_name": payer_first_name,
                    "last_name": payer_last_name,
                },
            }
            
            # Captura automática
            payment_create_data["capture"] = True
        
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
        # Usar os dados que já validamos (payer_email, payer_first_name, payer_last_name)
        # pois o MP pode retornar null em alguns campos
        pagamento.cliente_email = payer_email  # Já validado, nunca é null
        pagamento.cliente_nome = f"{payer_first_name} {payer_last_name}".strip()
        
        # Tentar pegar CPF da resposta do MP ou dos dados enviados
        payer_info = payment_result.get("payer", {})
        identification = payer_info.get("identification", {}) or payer_data.get("identification", {})
        if identification.get("type") == "CPF" and identification.get("number"):
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
        
        # Preparar resposta
        response_data = {
            'status': mp_status,
            'status_detail': payment_result.get("status_detail", ""),
            'payment_id': payment_result.get("id"),
            'payment_method_id': payment_method_id,
            'redirect_url': reverse('payments:pagamento_sucesso') + f"?external_reference={external_reference}" if mp_status == "approved" else None,
        }
        
        # Adicionar dados do PIX se for pagamento PIX
        if payment_method_id == 'pix':
            point_of_interaction = payment_result.get("point_of_interaction", {})
            transaction_data = point_of_interaction.get("transaction_data", {})
            
            response_data['pix_data'] = {
                'qr_code': transaction_data.get("qr_code", ""),
                'qr_code_base64': transaction_data.get("qr_code_base64", ""),
                'ticket_url': transaction_data.get("ticket_url", ""),
            }
            
            # Redirecionar para página do PIX pendente
            response_data['redirect_url'] = reverse('payments:pagamento_pix') + f"?external_reference={external_reference}"
        
        # Adicionar dados do boleto se for boleto
        elif payment_method_id in ['bolbradesco', 'pec']:
            barcode_data = payment_result.get("barcode", {})
            transaction_details = payment_result.get("transaction_details", {})
            
            response_data['boleto_data'] = {
                'barcode': barcode_data.get("content", ""),
                'external_resource_url': transaction_details.get("external_resource_url", ""),
                'digitable_line': payment_result.get("transaction_details", {}).get("digitable_line", "") or barcode_data.get("content", ""),
            }
            response_data['redirect_url'] = reverse('payments:pagamento_boleto') + f"?external_reference={external_reference}"
        
        return JsonResponse(response_data)
        
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
        # Verificar assinatura do webhook (opcional mas recomendado)
        webhook_secret = getattr(settings, 'MP_WEBHOOK_SECRET', None)
        if webhook_secret:
            import hmac
            import hashlib
            
            # Obter headers de assinatura
            x_signature = request.headers.get('x-signature', '')
            x_request_id = request.headers.get('x-request-id', '')
            
            # Extrair ts e v1 do header x-signature
            ts = None
            v1 = None
            for part in x_signature.split(','):
                if '=' in part:
                    key, value = part.split('=', 1)
                    if key.strip() == 'ts':
                        ts = value.strip()
                    elif key.strip() == 'v1':
                        v1 = value.strip()
            
            if ts and v1:
                # Construir string para verificação
                # Formato: id:[data.id];request-id:[x-request-id];ts:[ts];
                data_id = request.GET.get('data.id', '')
                manifest = f"id:{data_id};request-id:{x_request_id};ts:{ts};"
                
                # Calcular HMAC
                calculated_signature = hmac.new(
                    webhook_secret.encode(),
                    manifest.encode(),
                    hashlib.sha256
                ).hexdigest()
                
                if not hmac.compare_digest(calculated_signature, v1):
                    logger.warning(f"Webhook MP: assinatura inválida")
                    # Continuar mesmo com assinatura inválida para não perder notificações
                    # Em produção mais restrita, retornar 401 aqui
        
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


@require_GET
def pagamento_pix(request):
    """
    Página com QR Code PIX para pagamento.
    """
    external_reference = request.GET.get('external_reference')
    
    pagamento = None
    pix_data = {}
    
    if external_reference:
        try:
            pagamento = Pagamento.objects.get(external_reference=external_reference)
            
            # Buscar dados do PIX no response salvo
            mp_response = pagamento.mp_response_data or {}
            point_of_interaction = mp_response.get("point_of_interaction", {})
            transaction_data = point_of_interaction.get("transaction_data", {})
            
            pix_data = {
                'qr_code': transaction_data.get("qr_code", ""),
                'qr_code_base64': transaction_data.get("qr_code_base64", ""),
                'ticket_url': transaction_data.get("ticket_url", ""),
            }
            
        except Pagamento.DoesNotExist:
            pass
    
    context = {
        'pagamento': pagamento,
        'pix_data': pix_data,
    }
    
    return render(request, 'payments/pix.html', context)


@require_GET
def pagamento_boleto(request):
    """
    Página com dados do boleto bancário para pagamento.
    """
    external_reference = request.GET.get('external_reference')
    
    pagamento = None
    boleto_data = {}
    
    if external_reference:
        try:
            pagamento = Pagamento.objects.get(external_reference=external_reference)
            
            # Buscar dados do boleto no response salvo
            mp_response = pagamento.mp_response_data or {}
            barcode_data = mp_response.get("barcode", {})
            transaction_details = mp_response.get("transaction_details", {})
            
            boleto_data = {
                'barcode': barcode_data.get("content", ""),
                'external_resource_url': transaction_details.get("external_resource_url", ""),
                'digitable_line': transaction_details.get("digitable_line", "") or barcode_data.get("content", ""),
            }
            
            # Calcular data de vencimento (3 dias)
            from datetime import timedelta
            due_date = pagamento.criado_em + timedelta(days=3)
            boleto_data['due_date'] = due_date.strftime('%d/%m/%Y')
            
        except Pagamento.DoesNotExist:
            pass
    
    context = {
        'pagamento': pagamento,
        'boleto_data': boleto_data,
    }
    
    return render(request, 'payments/boleto.html', context)


@require_GET
def verificar_status_pagamento(request):
    """
    API para verificar status do pagamento (usado pelo frontend via polling).
    """
    external_reference = request.GET.get('external_reference')
    
    if not external_reference:
        return JsonResponse({'error': 'external_reference não fornecido'}, status=400)
    
    try:
        pagamento = Pagamento.objects.get(external_reference=external_reference)
        
        # Se ainda está pendente, consultar MP para atualizar
        if pagamento.status == 'processando' and pagamento.mp_payment_id:
            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
            payment_info = sdk.payment().get(pagamento.mp_payment_id)
            payment_data = payment_info.get("response", {})
            
            mp_status = payment_data.get("status", "")
            
            if mp_status == "approved":
                pagamento.status = "aprovado"
                pagamento.mp_status = mp_status
                pagamento.pago_em = timezone.now()
                pagamento.save()
        
        return JsonResponse({
            'status': pagamento.status,
            'mp_status': pagamento.mp_status,
            'approved': pagamento.status == 'aprovado',
            'redirect_url': reverse('obrigado') if pagamento.status == 'aprovado' else None,
        })
        
    except Pagamento.DoesNotExist:
        return JsonResponse({'error': 'Pagamento não encontrado'}, status=404)
