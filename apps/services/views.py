from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ProcessoAbertura, Socio
from .forms import (
    Etapa1DadosPessoaisForm, Etapa2EnderecoForm, Etapa3DadosEmpresaForm,
    SocioFormSet, Etapa5DocumentosForm, Etapa6InformacoesFiscaisForm,
    Etapa8AssinaturaForm, Etapa8RevisaoForm
)
from .pdf_generator import generate_contract_pdf


@login_required
def abertura_empresa_wizard(request, etapa=1):
    """
    View principal do wizard de abertura de empresa
    Gerencia todas as 8 etapas do processo
    """
    from .models import Plano
    
    # Busca ou cria um processo em andamento para o usuário
    processo, created = ProcessoAbertura.objects.get_or_create(
        usuario=request.user,
        status__in=['rascunho', 'em_andamento'],
        defaults={'etapa_atual': 1, 'status': 'em_andamento'}
    )
    
    # Validar se a etapa solicitada é válida
    if etapa < 1 or etapa > 8:
        messages.error(request, 'Etapa inválida.')
        return redirect('services:abertura_empresa', etapa=1)
    
    # Não permitir pular etapas
    if etapa > processo.etapa_atual + 1:
        messages.warning(request, 'Por favor, complete as etapas anteriores primeiro.')
        return redirect('services:abertura_empresa', etapa=processo.etapa_atual)
    
    # Selecionar o formulário da etapa atual
    form_class = get_form_for_etapa(etapa)
    
    form = None
    formset = None
    
    if request.method == 'POST':
        # Processar formulário
        if etapa == 4:  # Etapa de sócios usa formset
            formset = SocioFormSet(request.POST, prefix='socios')
            if formset.is_valid():
                # Deletar sócios existentes e criar novos
                processo.socios.all().delete()
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        socio = form.save(commit=False)
                        socio.processo = processo
                        socio.save()
                
                # Atualizar etapa
                if etapa >= processo.etapa_atual:
                    processo.etapa_atual = etapa + 1
                processo.save()
                
                messages.success(request, 'Dados dos sócios salvos com sucesso!')
                return redirect('services:abertura_empresa', etapa=etapa + 1)
        else:
            # Para etapas normais (ModelForm) ou a etapa 8 (Form simples)
            if etapa == 8:
                form = form_class(request.POST)
            else:
                form = form_class(request.POST, request.FILES, instance=processo)
                
            if form.is_valid():
                if etapa != 8: # Etapa 8 não salva no model via form
                    form.save()
                
                # Atualizar etapa
                if etapa >= processo.etapa_atual and etapa < 8:
                    processo.etapa_atual = etapa + 1
                
                # Etapa 7: registrar data de assinatura
                if etapa == 7:
                    processo.data_assinatura = timezone.now()
                
                # Etapa 8: Finalização
                if etapa == 8:
                    processo.status = 'em_analise' # Finalizado pelo cliente
                    processo.save()
                    messages.success(request, 'Processo de abertura enviado com sucesso! Nossa equipe entrará em contato.')
                    return redirect('services:processo_sucesso', processo_id=processo.id)
                
                processo.save()
                
                if etapa < 8:
                    messages.success(request, f'Etapa {etapa} concluída com sucesso!')
                    return redirect('services:abertura_empresa', etapa=etapa + 1)
    
    else:
        # GET: exibir formulário
        if etapa == 4:
            # Etapa de sócios: carregar sócios existentes
            initial_data = []
            for socio in processo.socios.all():
                initial_data.append({
                    'nome_completo': socio.nome_completo,
                    'cpf': socio.cpf,
                    'rg': socio.rg,
                    'estado_civil': socio.estado_civil,
                    'endereco_completo': socio.endereco_completo,
                    'percentual_participacao': socio.percentual_participacao,
                })
            
            # Se não houver sócios e quantidade_socios foi definida, criar forms vazios
            quantidade = processo.quantidade_socios or 1
            if not initial_data:
                initial_data = [{}] * quantidade
            
            formset = SocioFormSet(prefix='socios', initial=initial_data)
            form = None
        elif etapa == 8:
            form = form_class()
            formset = None
        else:
            form = form_class(instance=processo)
            formset = None
    
    # Calcular progresso
    progresso = (etapa / 8) * 100
    
    context = {
        'processo': processo,
        'etapa': etapa,
        'form': form,
        'formset': formset,
        'progresso': progresso,
        'total_etapas': 8,
    }
    
    return render(request, f'services/abertura_empresa/etapa_{etapa}.html', context)


def get_form_for_etapa(etapa):
    """Retorna a classe de formulário correspondente à etapa"""
    forms_map = {
        1: Etapa1DadosPessoaisForm,
        2: Etapa2EnderecoForm,
        3: Etapa3DadosEmpresaForm,
        # 4: SocioFormSet (tratado separadamente)
        5: Etapa5DocumentosForm,
        6: Etapa6InformacoesFiscaisForm,
        7: Etapa8AssinaturaForm,
        8: Etapa8RevisaoForm,
    }
    return forms_map.get(etapa)


@login_required
def pagamento_abertura(request, processo_id):
    """View para processar o pagamento do processo de abertura"""
    processo = get_object_or_404(ProcessoAbertura, id=processo_id, usuario=request.user)
    
    if not processo.plano_selecionado:
        messages.error(request, 'Nenhum plano foi selecionado.')
        return redirect('services:abertura_empresa', etapa=8)
    
    context = {
        'processo': processo,
        'plano': processo.plano_selecionado,
    }
    
    return render(request, 'services/abertura_empresa/pagamento.html', context)


@login_required
def confirmar_pagamento(request, processo_id):
    """View para confirmar pagamento (integração com gateway)"""
    processo = get_object_or_404(ProcessoAbertura, id=processo_id, usuario=request.user)
    
    # TODO: Implementar integração com Stripe/Mercado Pago
    # Por enquanto, apenas marcar como pago
    processo.pagamento_confirmado = True
    processo.data_pagamento = timezone.now()
    processo.status = 'em_analise'
    processo.save()
    
    messages.success(request, 'Pagamento confirmado! Seu processo está em análise.')
    return redirect('services:processo_sucesso', processo_id=processo.id)


@login_required
def processo_sucesso(request, processo_id):
    """View de sucesso após conclusão do processo"""
    processo = get_object_or_404(ProcessoAbertura, id=processo_id, usuario=request.user)
    
    context = {
        'processo': processo,
    }
    
    return render(request, 'services/abertura_empresa/sucesso.html', context)


@login_required
def buscar_cep(request):
    """API para buscar endereço por CEP usando ViaCEP"""
    import requests
    
    cep = request.GET.get('cep', '').replace('-', '').replace('.', '')
    
    if len(cep) != 8:
        return JsonResponse({'error': 'CEP inválido'}, status=400)
    
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        data = response.json()
        
        if 'erro' in data:
            return JsonResponse({'error': 'CEP não encontrado'}, status=404)
        
        return JsonResponse({
            'endereco': data.get('logradouro', ''),
            'bairro': data.get('bairro', ''),
            'cidade': data.get('localidade', ''),
            'estado': data.get('uf', ''),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def planos_view(request):
    """
    View para exibir os planos de abertura de empresa
    """
    from .models import Plano
    
    # Buscar planos ativos separados por categoria
    planos_servicos = Plano.objects.filter(ativo=True, categoria='servicos').order_by('preco')
    planos_comercio = Plano.objects.filter(ativo=True, categoria='comercio').order_by('preco')
    
    context = {
        'planos_servicos': planos_servicos,
        'planos_comercio': planos_comercio,
    }
    
    return render(request, 'services/planos.html', context)


def consulta_cnaes_view(request):
    """
    View para consulta de CNAEs usando a API do IBGE
    """
    import requests
    
    cnaes_data = []
    error_message = None
    
    try:
        # Buscar CNAEs da API do IBGE
        response = requests.get('https://servicodados.ibge.gov.br/api/v2/cnae/classes', timeout=10)
        
        if response.status_code == 200:
            cnaes_api = response.json()
            
            # Processar e organizar os dados
            for cnae in cnaes_api:
                cnaes_data.append({
                    'id': cnae.get('id'),
                    'descricao': cnae.get('descricao', 'Sem descrição'),
                    'observacoes': cnae.get('observacoes', ''),
                })
        else:
            error_message = f'Erro ao buscar CNAEs: Status {response.status_code}'
            
    except requests.exceptions.Timeout:
        error_message = 'Tempo esgotado ao conectar com a API do IBGE. Tente novamente.'
    except requests.exceptions.RequestException as e:
        error_message = f'Erro ao conectar com a API do IBGE: {str(e)}'
    except Exception as e:
        error_message = f'Erro inesperado: {str(e)}'
    
    context = {
        'cnaes': cnaes_data,
        'total_cnaes': len(cnaes_data),
        'error_message': error_message,
    }
    
    return render(request, 'services/consultar_cnaes.html', context)


def calculadora_clt_pj(request):
    """
    Calculadora de Salário CLT vs. PJ
    Compara o salário líquido entre os dois regimes
    """
    resultados = None
    salario_bruto = None
    
    if request.method == 'POST':
        try:
            salario_bruto = float(request.POST.get('salario_bruto', 0))
            
            if salario_bruto <= 0:
                messages.error(request, 'Por favor, informe um salário válido.')
            else:
                # ===== CÁLCULO CLT =====
                # 1. INSS (2024)
                inss = 0
                if salario_bruto <= 1412.00:
                    inss = salario_bruto * 0.075
                elif salario_bruto <= 2666.68:
                    inss = 1412.00 * 0.075 + (salario_bruto - 1412.00) * 0.09
                elif salario_bruto <= 4000.03:
                    inss = 1412.00 * 0.075 + (2666.68 - 1412.00) * 0.09 + (salario_bruto - 2666.68) * 0.12
                else:
                    inss = 1412.00 * 0.075 + (2666.68 - 1412.00) * 0.09 + (4000.03 - 2666.68) * 0.12 + (salario_bruto - 4000.03) * 0.14
                    # Teto máximo do INSS
                    inss = min(inss, 908.85)
                
                # 2. Base de cálculo do IRRF (salário - INSS)
                base_irrf = salario_bruto - inss
                
                # 3. IRRF (2024) - considerando dedução padrão
                deducao_dependentes = 0  # Simplificado: sem dependentes
                base_irrf -= deducao_dependentes
                
                irrf = 0
                if base_irrf <= 2259.20:
                    irrf = 0
                elif base_irrf <= 2826.65:
                    irrf = base_irrf * 0.075 - 169.44
                elif base_irrf <= 3751.05:
                    irrf = base_irrf * 0.15 - 381.44
                elif base_irrf <= 4664.68:
                    irrf = base_irrf * 0.225 - 662.77
                else:
                    irrf = base_irrf * 0.275 - 896.00
                
                irrf = max(irrf, 0)
                
                # Salário líquido CLT
                salario_liquido_clt = salario_bruto - inss - irrf
                
                # Benefícios CLT (não entram no líquido, mas são vantagens)
                decimo_terceiro = salario_bruto
                ferias = salario_bruto + (salario_bruto / 3)  # + 1/3
                fgts_mensal = salario_bruto * 0.08
                fgts_anual = fgts_mensal * 12
                
                # ===== CÁLCULO PJ (Simples Nacional - Anexo III) =====
                # Alíquota inicial de 6% (simplificado)
                aliquota_simples = 0.06
                imposto_pj = salario_bruto * aliquota_simples
                salario_liquido_pj = salario_bruto - imposto_pj
                
                # Diferença
                diferenca = salario_liquido_pj - salario_liquido_clt
                diferenca_percentual = (diferenca / salario_liquido_clt) * 100 if salario_liquido_clt > 0 else 0
                
                # Contexto de resultados
                resultados = {
                    'salario_bruto': salario_bruto,
                    # CLT
                    'clt_inss': inss,
                    'clt_irrf': irrf,
                    'clt_total_descontos': inss + irrf,
                    'clt_salario_liquido': salario_liquido_clt,
                    'clt_decimo_terceiro': decimo_terceiro,
                    'clt_ferias': ferias,
                    'clt_fgts_anual': fgts_anual,
                    # PJ
                    'pj_imposto': imposto_pj,
                    'pj_aliquota': aliquota_simples * 100,
                    'pj_salario_liquido': salario_liquido_pj,
                    # Comparação
                    'diferenca': diferenca,
                    'diferenca_percentual': diferenca_percentual,
                }
                
        except (ValueError, TypeError):
            messages.error(request, 'Por favor, informe um valor numérico válido.')
    
    context = {
        'resultados': resultados,
        'salario_bruto': salario_bruto,
    }
    
    return render(request, 'recursos/calculadora_clt_pj.html', context)


@login_required
def download_contrato(request, processo_id):
    """
    Gera e retorna o PDF do contrato assinado
    """
    processo = get_object_or_404(ProcessoAbertura, id=processo_id, usuario=request.user)
    
    if not processo.assinatura_digital:
        messages.warning(request, 'O contrato ainda não foi assinado.')
        return redirect('services:abertura_empresa', etapa=7)
        
    pdf_buffer = generate_contract_pdf(processo)
    
    return FileResponse(
        pdf_buffer, 
        as_attachment=True, 
        filename=f'contrato_prestacao_servicos_{processo.id}.pdf'
    )

def contrato_test_view(request):
    """
    View de teste para gerar o contrato PDF com dados manuais
    """
    if request.method == 'POST':
        # Criar um objeto mockado com os dados do form
        class ProcessoMock:
            def __init__(self, data):
                self.nome_completo = data.get('nome_completo')
                self.cpf = data.get('cpf')
                self.endereco = data.get('endereco')
                self.numero = data.get('numero')
                self.bairro = data.get('bairro')
                self.cidade = data.get('cidade')
                self.estado = data.get('estado')
                self.assinatura_digital = None # Para teste sem assinatura
                # O pdf_generator pode precisar de mais campos se for atualizado,
                # por enquanto estes são os usados.
        
        processo_mock = ProcessoMock(request.POST)
        
        # Gerar o PDF
        pdf_buffer = generate_contract_pdf(processo_mock)
        
        return FileResponse(
            pdf_buffer,
            as_attachment=False,
            filename='contrato_teste.pdf'
        )
        
    return render(request, 'contrato_test.html')

def servicos_view(request):
    """
    View para a página de serviços (segmentos/servicos)
    Lista os planos disponíveis.
    """
    from .models import Plano
    planos_servicos = Plano.objects.filter(categoria='servicos', ativo=True).order_by('ordem', 'preco')
    planos_comercio = Plano.objects.filter(categoria='comercio', ativo=True).order_by('ordem', 'preco')
    
    context = {
        'planos_servicos': planos_servicos,
        'planos_comercio': planos_comercio,
    }
    
    return render(request, 'segments/servicos.html', context)


# =============================================================================
# VIEWS DE ABERTURA MEI (Página /abrir-mei/)
# =============================================================================

def abrir_mei_view(request):
    """
    View da Landing Page de Abertura de MEI.
    Exibe informações sobre o serviço e planos.
    """
    from apps.testimonials.models import Testimonial
    
    # Buscar depoimentos para exibir na página
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'testimonials': testimonials,
    }
    
    return render(request, 'services/abrir_mei.html', context)

def contabilidade_mei_view(request):
    """
    View da Landing Page de Contabilidade para MEI.
    Exibe planos específicos para MEI e depoimentos.
    """
    from apps.testimonials.models import Testimonial
    from .models import Plano
    
    # Buscar planos MEI
    planos_mei = Plano.objects.filter(ativo=True, categoria='mei').order_by('ordem', 'preco')

    # Buscar depoimentos
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'planos_mei': planos_mei,
        'testimonials': testimonials,
    }
    
    return render(request, 'services/contabilidade_mei.html', context)


def solicitar_abertura_mei_view(request):
    """
    View do formulário de cadastro para Abertura de MEI.
    Ao submeter o formulário com sucesso, redireciona para a página de pagamento.
    Valor do serviço: R$ 129,90
    """
    from .forms import AberturaMEIForm
    from .models import SolicitacaoAberturaMEI
    
    if request.method == 'POST':
        form = AberturaMEIForm(request.POST)
        
        if form.is_valid():
            # Salvar a solicitação no banco de dados
            solicitacao = form.save(commit=False)
            solicitacao.status = 'pendente'
            solicitacao.save()
            
            # Armazenar o ID da solicitação na sessão para uso na página de pagamento
            request.session['solicitacao_mei_id'] = solicitacao.id
            
            # Verificar se já está autenticado
            if not request.user.is_authenticated:
                # Redirecionar para criação de usuário
                messages.success(
                    request, 
                    'Dados iniciais salvos! Crie sua conta ou faça login para finalizar o pedido.'
                )
                return redirect('services:register_mei', solicitacao_id=solicitacao.id)
            
            # Adicionar mensagem de sucesso
            messages.success(
                request, 
                'Dados salvos com sucesso! Agora finalize o pagamento para iniciar o processo de abertura do seu MEI.'
            )
            
            # Redirecionar para a página de checkout/pagamento
            return redirect('services:checkout_mei', solicitacao_id=solicitacao.id)
        else:
            # Se o formulário tiver erros, exibir mensagem
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = AberturaMEIForm()
    
    context = {
        'form': form,
        'valor_servico': SolicitacaoAberturaMEI.VALOR_SERVICO,
    }
    
    return render(request, 'services/abrir_mei_form.html', context)


def contratar_plano_mei_view(request):
    """
    View para processar a escolha de plano da página Contabilidade MEI.
    Redireciona para o formulário de contratação ou WhatsApp com a mensagem pronta.
    """
    plano = "Básico"
    if 'planosecundar' in request.GET:
        plano = "Profissional"
    elif 'planopremium' in request.GET:
        plano = "Premium"
        
    # Aqui você pode redirecionar para um checkout ou form de contato
    # Por enquanto, vou redirecionar para o WhatsApp com uma mensagem personalizada
    
    texto = f"Olá! Gostaria de contratar o Plano {plano} para Contabilidade MEI."
    import urllib.parse
    texto_encoded = urllib.parse.quote(texto)
    
    url_whatsapp = f"https://wa.me/551131642284?text={texto_encoded}"
    
    return redirect(url_whatsapp)


def register_mei_view(request, solicitacao_id):
    """
    View para cadastro/login de usuário durante o fluxo de MEI
    """
    from django.contrib.auth import login, get_user_model, authenticate
    from django.contrib.auth.password_validation import validate_password
    from django.core.exceptions import ValidationError as DjangoValidationError
    from .models import SolicitacaoAberturaMEI
    
    User = get_user_model()
    solicitacao = get_object_or_404(SolicitacaoAberturaMEI, id=solicitacao_id)
    
    if request.user.is_authenticated:
        return redirect('services:checkout_mei', solicitacao_id=solicitacao.id)
    
    if request.method == 'POST':
        action = request.POST.get('action') # 'register' ou 'login'
        
        if action == 'register':
            first_name = request.POST.get('first_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validações básicas
            if not all([first_name, email, password, confirm_password]):
                messages.error(request, 'Preencha todos os campos.')
            elif password != confirm_password:
                messages.error(request, 'As senhas não conferem.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Este e-mail já está cadastrado. Faça login.')
            else:
                try:
                    # Validar senha
                    validate_password(password)
                    
                    # Criar usuário
                    username = email # Username é o email
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name
                    )
                    
                    # Login automático
                    login(request, user)
                    
                    messages.success(request, 'Conta criada com sucesso!')
                    return redirect('services:checkout_mei', solicitacao_id=solicitacao.id)
                    
                except DjangoValidationError as e:
                    for error in e.messages:
                        messages.error(request, error)
                except Exception as e:
                    messages.error(request, 'Erro ao criar conta. Tente novamente.')
                    print(f"Erro register MEI: {e}")
                    
        elif action == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {user.first_name}!')
                return redirect('services:checkout_mei', solicitacao_id=solicitacao.id)
            else:
                messages.error(request, 'E-mail ou senha inválidos.')

    context = {
        'solicitacao': solicitacao,
    }
    return render(request, 'services/register_mei.html', context)


@login_required
def checkout_mei_view(request, solicitacao_id):
    """
    Página de checkout/pagamento para abertura de MEI.
    Exibe resumo da solicitação e opções de pagamento.
    Valor fixo: R$ 2,00
    """
    from .models import SolicitacaoAberturaMEI
    from apps.payments.models import Pagamento
    import mercadopago
    from django.conf import settings
    
    # Buscar a solicitação
    solicitacao = get_object_or_404(SolicitacaoAberturaMEI, id=solicitacao_id)
    
    # Verificar se o ID na sessão corresponde (segurança básica)
    session_id = request.session.get('solicitacao_mei_id')
    # Se admin/staff, permite visualizar. Se usuário comum, valida sessão OU dono
    if not request.user.is_staff and session_id != solicitacao.id:
        # Se usuário logado e CPF bate com a solicitação (opcional)
        # Por enquanto mantemos a lógica simples:
        messages.warning(request, 'Você precisa preencher o formulário para acessar o pagamento.')
        return redirect('services:abrir_mei')
    
    # Verificar se já foi pago
    if solicitacao.status == 'pago':
        messages.info(request, 'Esta solicitação já foi paga.')
        return redirect('services:mei_sucesso', solicitacao_id=solicitacao.id)

    # ----------------------------------------------------
    # Integração Mercado Pago
    # ----------------------------------------------------
    
    # 1. Recuperar ou criar Pagamento
    if not solicitacao.pagamento:
        pagamento = Pagamento.objects.create(
            valor=solicitacao.VALOR_SERVICO,
            status='pendente',
            cliente=request.user if request.user.is_authenticated else None,
            cliente_nome=solicitacao.nome_completo,
            cliente_email=solicitacao.email,
            cliente_cpf=solicitacao.cpf,
        )
        solicitacao.pagamento = pagamento
        solicitacao.save()
    else:
        pagamento = solicitacao.pagamento
        # Atualiza valor caso tenha mudado (improvável para este caso, mas boa prática)
        if pagamento.valor != solicitacao.VALOR_SERVICO and pagamento.status == 'pendente':
            pagamento.valor = solicitacao.VALOR_SERVICO
            pagamento.save()

    # 2. Configurar SDK e Preferência
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    site_url = settings.SITE_URL.rstrip('/')
    notification_url = f"{site_url}/payments/webhook/mercadopago/"

    # Preferência
    preference_data = {
        "items": [
            {
                "id": f"MEI-{solicitacao.id}",
                "title": f"Abertura MEI - {solicitacao.nome_completo}",
                "description": f"Serviço de Abertura de MEI para {solicitacao.nome_completo}",
                "category_id": "services",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(solicitacao.VALOR_SERVICO)
            }
        ],
        "external_reference": str(pagamento.external_reference),
        "statement_descriptor": "VETORIAL MEI",
        "notification_url": notification_url,
        "payer": {
            "name": solicitacao.nome_completo,
            "email": solicitacao.email,
            "identification": {
                "type": "CPF",
                "number": ''.join(filter(str.isdigit, solicitacao.cpf))
            }
        },
        "back_urls": {
            "success": f"{site_url}/services/abrir-mei/sucesso/{solicitacao.id}/",
            "failure": f"{site_url}/services/abrir-mei/checkout/{solicitacao.id}/",
            "pending": f"{site_url}/services/abrir-mei/checkout/{solicitacao.id}/"
        },
        "auto_return": "approved",
    }
    
    preference_id = None
    try:
        # Tenta criar/atualizar preferência apenas se não tiver ID salvo ou se quiser renovar
        # Aqui criaremos sempre uma nova para garantir dados atualizados ou usar a do pagamento se validada
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})
        preference_id = preference.get("id")
        
        if preference_id:
            pagamento.mp_preference_id = preference_id
            pagamento.save()
        else:
             # Log erro
            print(f"Erro MP Create Preference: {preference_response}")

    except Exception as e:
        print(f"Exception MP: {e}")

    context = {
        'solicitacao': solicitacao,
        'valor_servico': solicitacao.VALOR_SERVICO,
        'pagamento': pagamento,
        'preference_id': preference_id,
        'mp_public_key': settings.MERCADO_PAGO_PUBLIC_KEY,
        'site_url': site_url,
    }
    
    return render(request, 'services/checkout_mei.html', context)


def processar_pagamento_mei(request, solicitacao_id):
    """
    Processa o pagamento da abertura de MEI.
    Esta view será integrada com o gateway de pagamento (Mercado Pago).
    Por enquanto, apenas marca como processando e redireciona.
    """
    from .models import SolicitacaoAberturaMEI
    
    if request.method != 'POST':
        return redirect('services:checkout_mei', solicitacao_id=solicitacao_id)
    
    solicitacao = get_object_or_404(SolicitacaoAberturaMEI, id=solicitacao_id)
    
    # Verificar se já foi pago
    if solicitacao.status == 'pago':
        messages.info(request, 'Esta solicitação já foi paga.')
        return redirect('services:mei_sucesso', solicitacao_id=solicitacao.id)
    
    # TODO: Integração com Mercado Pago
    # Por enquanto, criar uma preferência de pagamento fictícia
    # e redirecionar para a página de sucesso para demonstração
    
    # Integração com Mercado Pago (quando implementado):
    # 1. Criar preferência de pagamento
    # 2. Redirecionar para o checkout do Mercado Pago
    # 3. Webhook receberá a confirmação do pagamento
    
    # Para demonstração, marcar como pago
    # Em produção, isso será feito pelo webhook do gateway
    solicitacao.status = 'pago'
    solicitacao.save()
    
    messages.success(request, 'Pagamento processado com sucesso!')
    return redirect('obrigado')


def mei_sucesso_view(request, solicitacao_id):
    """
    Página de sucesso após pagamento da abertura de MEI.
    Exibe confirmação e próximos passos.
    """
    from .models import SolicitacaoAberturaMEI
    
    solicitacao = get_object_or_404(SolicitacaoAberturaMEI, id=solicitacao_id)

    # Verifica status do pagamento vinculado para atualizar a solicitação se necessário
    if solicitacao.pagamento: 
        status_pagamento = solicitacao.pagamento.status
        # Se o pagamento foi aprovado mas a solicitação ainda consta pendente
        if status_pagamento == 'aprovado' and solicitacao.status == 'pendente':
            solicitacao.status = 'pago'
            solicitacao.save()
        # Se for processando (Pix pode demorar segundos ou estar em processamento)
        elif status_pagamento == 'processando' and solicitacao.status == 'pendente':
            # Mantém pendente ou muda para um status intermediário se houver
            pass
    
    # Limpar a sessão
    if 'solicitacao_mei_id' in request.session:
        del request.session['solicitacao_mei_id']
    
    context = {
        'solicitacao': solicitacao,
    }
    
    return render(request, 'services/mei_sucesso.html', context)


# ==============================================================
# BAIXA DO MEI - Fluxo completo (formulário → checkout → sucesso)
# ==============================================================

@csrf_exempt
def solicitar_baixa_mei_view(request):
    """
    View do formulário de Baixa do MEI.
    Recebe JSON via fetch, salva a solicitação e retorna URL do checkout.
    """
    from .models import SolicitacaoBaixaMEI

    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

    try:
        import json
        data = json.loads(request.body)

        solicitacao = SolicitacaoBaixaMEI.objects.create(
            nome_completo=data.get('nome_completo', ''),
            email=data.get('email', ''),
            telefone=data.get('telefone', ''),
            cnpj=data.get('cnpj', ''),
            cpf=data.get('cpf', ''),
            motivo=data.get('motivo', ''),
            observacoes=data.get('observacoes', ''),
            status='pendente',
        )

        request.session['solicitacao_baixa_mei_id'] = solicitacao.id

        return JsonResponse({
            'success': True,
            'redirect_url': f'/services/baixar-mei/checkout/{solicitacao.id}/'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def checkout_baixa_mei_view(request, solicitacao_id):
    """
    Página de checkout/pagamento para Baixa do MEI.
    Valor fixo: R$ 129,90
    """
    from .models import SolicitacaoBaixaMEI
    from apps.payments.models import Pagamento
    import mercadopago
    from django.conf import settings as django_settings

    solicitacao = get_object_or_404(SolicitacaoBaixaMEI, id=solicitacao_id)

    session_id = request.session.get('solicitacao_baixa_mei_id')
    if not request.user.is_staff and session_id != solicitacao.id:
        messages.warning(request, 'Você precisa preencher o formulário para acessar o pagamento.')
        return redirect('baixar_mei')

    if solicitacao.status == 'pago':
        messages.info(request, 'Esta solicitação já foi paga.')
        return redirect('services:baixa_mei_sucesso', solicitacao_id=solicitacao.id)

    # Criar ou recuperar Pagamento
    if not solicitacao.pagamento:
        pagamento = Pagamento.objects.create(
            valor=solicitacao.VALOR_SERVICO,
            status='pendente',
            cliente=request.user if request.user.is_authenticated else None,
            cliente_nome=solicitacao.nome_completo,
            cliente_email=solicitacao.email,
            cliente_cpf=solicitacao.cpf,
        )
        solicitacao.pagamento = pagamento
        solicitacao.save()
    else:
        pagamento = solicitacao.pagamento

    # Mercado Pago
    sdk = mercadopago.SDK(django_settings.MERCADO_PAGO_ACCESS_TOKEN)
    site_url = django_settings.SITE_URL.rstrip('/')
    notification_url = f"{site_url}/payments/webhook/mercadopago/"

    preference_data = {
        "items": [{
            "id": f"BAIXA-MEI-{solicitacao.id}",
            "title": f"Baixa do MEI - {solicitacao.nome_completo}",
            "description": f"Serviço de Baixa (Cancelamento) do MEI - CNPJ: {solicitacao.cnpj}",
            "category_id": "services",
            "quantity": 1,
            "currency_id": "BRL",
            "unit_price": float(solicitacao.VALOR_SERVICO)
        }],
        "external_reference": str(pagamento.external_reference),
        "statement_descriptor": "VETORIAL MEI",
        "notification_url": notification_url,
        "payer": {
            "name": solicitacao.nome_completo,
            "email": solicitacao.email,
            "identification": {
                "type": "CPF",
                "number": ''.join(filter(str.isdigit, solicitacao.cpf))
            }
        },
        "back_urls": {
            "success": f"{site_url}/services/baixar-mei/sucesso/{solicitacao.id}/",
            "failure": f"{site_url}/services/baixar-mei/checkout/{solicitacao.id}/",
            "pending": f"{site_url}/services/baixar-mei/checkout/{solicitacao.id}/"
        },
        "auto_return": "approved",
    }

    preference_id = None
    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})
        preference_id = preference.get("id")
        if preference_id:
            pagamento.mp_preference_id = preference_id
            pagamento.save()
    except Exception as e:
        print(f"Exception MP Baixa MEI: {e}")

    context = {
        'solicitacao': solicitacao,
        'valor_servico': solicitacao.VALOR_SERVICO,
        'pagamento': pagamento,
        'preference_id': preference_id,
        'mp_public_key': django_settings.MERCADO_PAGO_PUBLIC_KEY,
        'site_url': site_url,
        'tipo_servico': 'baixa_mei',
        'titulo_servico': 'Baixa do MEI',
        'descricao_servico': 'Cancelamento do CNPJ MEI',
        'icone_servico': 'bi-x-circle',
        'cor_tema': '#db2777',
        'url_voltar': '/baixar-mei/',
        'url_sucesso': f'/services/baixar-mei/sucesso/{solicitacao.id}/',
        'itens_incluidos': [
            'Cancelamento do CNPJ MEI',
            'Baixa na Junta Comercial',
            'Cancelamento na Prefeitura',
            'Emissão do certificado de baixa',
            'Orientação sobre obrigações pendentes',
            'Suporte por WhatsApp',
        ],
    }

    return render(request, 'services/checkout_servico_mei.html', context)


def baixa_mei_sucesso_view(request, solicitacao_id):
    """Página de sucesso após pagamento da Baixa do MEI."""
    from .models import SolicitacaoBaixaMEI

    solicitacao = get_object_or_404(SolicitacaoBaixaMEI, id=solicitacao_id)

    if solicitacao.pagamento:
        if solicitacao.pagamento.status == 'aprovado' and solicitacao.status == 'pendente':
            solicitacao.status = 'pago'
            solicitacao.save()

    if 'solicitacao_baixa_mei_id' in request.session:
        del request.session['solicitacao_baixa_mei_id']

    context = {
        'solicitacao': solicitacao,
        'titulo_servico': 'Baixa do MEI',
        'descricao_sucesso': 'Sua solicitação de cancelamento do MEI foi recebida com sucesso!',
        'cor_tema': '#db2777',
    }

    return render(request, 'services/sucesso_servico_mei.html', context)


# ==============================================================
# DECLARAÇÃO ANUAL MEI (DASN) - Fluxo completo
# ==============================================================

@csrf_exempt
def solicitar_declaracao_anual_mei_view(request):
    """
    View do formulário de Declaração Anual MEI.
    Recebe JSON via fetch, salva a solicitação e retorna URL do checkout.
    """
    from .models import SolicitacaoDeclaracaoAnualMEI

    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

    try:
        import json
        from decimal import Decimal
        data = json.loads(request.body)

        faturamento_str = data.get('faturamento', '0')
        if isinstance(faturamento_str, str):
            faturamento_str = faturamento_str.replace('.', '').replace(',', '.')
        faturamento = Decimal(faturamento_str) if faturamento_str else Decimal('0')

        solicitacao = SolicitacaoDeclaracaoAnualMEI.objects.create(
            nome_completo=data.get('nome_completo', ''),
            email=data.get('email', ''),
            telefone=data.get('telefone', ''),
            cnpj=data.get('cnpj', ''),
            ano_referencia=data.get('ano_referencia', ''),
            faturamento=faturamento,
            teve_funcionario=data.get('teve_funcionario', False),
            observacoes=data.get('observacoes', ''),
            status='pendente',
        )

        request.session['solicitacao_dasn_mei_id'] = solicitacao.id

        return JsonResponse({
            'success': True,
            'redirect_url': f'/services/declaracao-anual-mei/checkout/{solicitacao.id}/'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def checkout_declaracao_anual_mei_view(request, solicitacao_id):
    """
    Página de checkout/pagamento para Declaração Anual MEI (DASN-SIMEI).
    Valor fixo: R$ 89,90
    """
    from .models import SolicitacaoDeclaracaoAnualMEI
    from apps.payments.models import Pagamento
    import mercadopago
    from django.conf import settings as django_settings

    solicitacao = get_object_or_404(SolicitacaoDeclaracaoAnualMEI, id=solicitacao_id)

    session_id = request.session.get('solicitacao_dasn_mei_id')
    if not request.user.is_staff and session_id != solicitacao.id:
        messages.warning(request, 'Você precisa preencher o formulário para acessar o pagamento.')
        return redirect('declaracao_anual_mei')

    if solicitacao.status == 'pago':
        messages.info(request, 'Esta solicitação já foi paga.')
        return redirect('services:dasn_mei_sucesso', solicitacao_id=solicitacao.id)

    # Criar ou recuperar Pagamento
    if not solicitacao.pagamento:
        pagamento = Pagamento.objects.create(
            valor=solicitacao.VALOR_SERVICO,
            status='pendente',
            cliente=request.user if request.user.is_authenticated else None,
            cliente_nome=solicitacao.nome_completo,
            cliente_email=solicitacao.email,
        )
        solicitacao.pagamento = pagamento
        solicitacao.save()
    else:
        pagamento = solicitacao.pagamento

    # Mercado Pago
    sdk = mercadopago.SDK(django_settings.MERCADO_PAGO_ACCESS_TOKEN)
    site_url = django_settings.SITE_URL.rstrip('/')
    notification_url = f"{site_url}/payments/webhook/mercadopago/"

    preference_data = {
        "items": [{
            "id": f"DASN-MEI-{solicitacao.id}",
            "title": f"Declaração Anual MEI (DASN) - {solicitacao.nome_completo}",
            "description": f"Declaração Anual MEI - CNPJ: {solicitacao.cnpj} - Ano: {solicitacao.ano_referencia}",
            "category_id": "services",
            "quantity": 1,
            "currency_id": "BRL",
            "unit_price": float(solicitacao.VALOR_SERVICO)
        }],
        "external_reference": str(pagamento.external_reference),
        "statement_descriptor": "VETORIAL DASN",
        "notification_url": notification_url,
        "payer": {
            "name": solicitacao.nome_completo,
            "email": solicitacao.email,
        },
        "back_urls": {
            "success": f"{site_url}/services/declaracao-anual-mei/sucesso/{solicitacao.id}/",
            "failure": f"{site_url}/services/declaracao-anual-mei/checkout/{solicitacao.id}/",
            "pending": f"{site_url}/services/declaracao-anual-mei/checkout/{solicitacao.id}/"
        },
        "auto_return": "approved",
    }

    preference_id = None
    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})
        preference_id = preference.get("id")
        if preference_id:
            pagamento.mp_preference_id = preference_id
            pagamento.save()
    except Exception as e:
        print(f"Exception MP DASN MEI: {e}")

    context = {
        'solicitacao': solicitacao,
        'valor_servico': solicitacao.VALOR_SERVICO,
        'pagamento': pagamento,
        'preference_id': preference_id,
        'mp_public_key': django_settings.MERCADO_PAGO_PUBLIC_KEY,
        'site_url': site_url,
        'tipo_servico': 'dasn_mei',
        'titulo_servico': 'Declaração Anual MEI (DASN-SIMEI)',
        'descricao_servico': 'Declaração Anual do Simples Nacional',
        'icone_servico': 'bi-file-earmark-text',
        'cor_tema': '#059669',
        'url_voltar': '/declaracao-anual-mei/',
        'url_sucesso': f'/services/declaracao-anual-mei/sucesso/{solicitacao.id}/',
        'itens_incluidos': [
            'Preenchimento da DASN-SIMEI',
            'Cálculo do faturamento anual',
            'Transmissão à Receita Federal',
            'Emissão do recibo de entrega',
            'Verificação de pendências',
            'Suporte por WhatsApp',
        ],
    }

    return render(request, 'services/checkout_servico_mei.html', context)


def dasn_mei_sucesso_view(request, solicitacao_id):
    """Página de sucesso após pagamento da Declaração Anual MEI."""
    from .models import SolicitacaoDeclaracaoAnualMEI

    solicitacao = get_object_or_404(SolicitacaoDeclaracaoAnualMEI, id=solicitacao_id)

    if solicitacao.pagamento:
        if solicitacao.pagamento.status == 'aprovado' and solicitacao.status == 'pendente':
            solicitacao.status = 'pago'
            solicitacao.save()

    if 'solicitacao_dasn_mei_id' in request.session:
        del request.session['solicitacao_dasn_mei_id']

    context = {
        'solicitacao': solicitacao,
        'titulo_servico': 'Declaração Anual MEI (DASN-SIMEI)',
        'descricao_sucesso': 'Sua solicitação de Declaração Anual MEI foi recebida com sucesso!',
        'cor_tema': '#059669',
    }

    return render(request, 'services/sucesso_servico_mei.html', context)