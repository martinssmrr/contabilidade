from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from django.utils import timezone
from decimal import Decimal, InvalidOperation
import random
from django.core.mail import send_mail
from django.urls import reverse

from .models import MovimentacaoFinanceira
from .models import TransmissaoMensal
from .models import CertidaoNegativa
from apps.documents.models_guia_imposto import GuiaImposto
from django.db.models import Sum, Q
from django.conf import settings
from .utils import validate_file_upload

User = get_user_model()


def login_view(request):
    """View para login de usuários"""
    if request.user.is_authenticated:
        return redirect('users:area_cliente')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'users:area_cliente')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos. Por favor, tente novamente.')
    
    return render(request, 'users/login.html')


def register_view(request):
    """View para cadastro de novos usuários"""
    if request.user.is_authenticated:
        return redirect('users:area_cliente')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validações
        if not all([first_name, email, password, password_confirm]):
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'users/register.html')
        
        if password != password_confirm:
            messages.error(request, 'As senhas não coincidem. Por favor, tente novamente.')
            return render(request, 'users/register.html')
        
        # Validar senha usando os validadores do Django
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError as DjangoValidationError
        try:
            validate_password(password)
        except DjangoValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'users/register.html')
        
        # Verificar se email já existe
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado. Por favor, faça login ou use outro email.')
            return render(request, 'users/register.html')
        
        # Verificar se username (email) já existe
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Este email já está cadastrado. Por favor, faça login ou use outro email.')
            return render(request, 'users/register.html')
        
        try:
            # Criar usuário
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name
            )
            
            # Fazer login automático
            login(request, user)
            messages.success(request, f'Bem-vindo, {first_name}! Sua conta foi criada com sucesso.')
            return redirect('users:area_cliente')
            
        except IntegrityError:
            messages.error(request, 'Erro ao criar conta. Por favor, tente novamente.')
            return render(request, 'users/register.html')
    
    return render(request, 'users/register.html')


@login_required
def logout_view(request):
    """View para logout de usuários"""
    user_name = request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f'Até logo, {user_name}! Você saiu com sucesso.')
    return redirect('home')


@login_required
def area_cliente(request):
    """View para a área do cliente - Painel de Controle"""
    return render(request, 'users/area_cliente_new.html')


@login_required
def api_contabilidade_summary(request):
    """Retorna resumo contábil para o mês atual: total receitas, despesas e resultado,
    e informações sobre a última transmissão do usuário.
    """
    user = request.user
    from django.utils import timezone
    now = timezone.localtime()
    year = now.year
    month = now.month

    qs = MovimentacaoFinanceira.objects.filter(user=user, competencia__year=year, competencia__month=month)
    total_receitas = qs.filter(tipo='receita').aggregate(total=Sum('valor'))['total'] or 0
    total_despesas = qs.filter(tipo='despesa').aggregate(total=Sum('valor'))['total'] or 0
    resultado = total_receitas - total_despesas

    # última transmissão do usuário
    last_trans = TransmissaoMensal.objects.filter(user=user).order_by('-transmitted_at').first()
    last_trans_data = None
    if last_trans:
        last_trans_data = {
            'id': last_trans.id,
            'competencia': last_trans.competencia.strftime('%Y-%m'),
            'transmitted_at': last_trans.transmitted_at.isoformat(),
            'count': last_trans.movimentacoes.count(),
        }

    return JsonResponse({
        'success': True,
        'receitas': str(total_receitas),
        'despesas': str(total_despesas),
        'resultado': str(resultado),
        'last_transmissao': last_trans_data,
    })


@login_required
def api_certidoes_status(request):
    """Retorna o status mais recente das quatro certidões do cliente."""
    user = request.user
    def last(tipo):
        try:
            return CertidaoNegativa.objects.filter(cliente=user, tipo=tipo).latest('data_envio')
        except CertidaoNegativa.DoesNotExist:
            return None

    items = []
    tipos = [
        (CertidaoNegativa.TIPO_FEDERAL, 'Federal'),
        (CertidaoNegativa.TIPO_ESTADUAL, 'Estadual'),
        (CertidaoNegativa.TIPO_TRABALHISTA, 'Trabalhista'),
        (CertidaoNegativa.TIPO_FGTS, 'FGTS'),
    ]
    has_indisponivel = False
    for key, label in tipos:
        c = last(key)
        status = c.status if c else None
        if status == CertidaoNegativa.STATUS_INDISPONIVEL:
            has_indisponivel = True
        items.append({
            'tipo': key,
            'label': label,
            'status': status,
            'status_display': c.get_status_display() if c else 'Sem Registro',
            'data_envio': c.data_envio.isoformat() if c else None,
            'arquivo_url': c.arquivo_pdf.url if c and c.arquivo_pdf else None,
        })

    return JsonResponse({'success': True, 'items': items, 'has_indisponivel': has_indisponivel})


@login_required
def notas_fiscais(request):
    """
    View para exibir o menu de notas fiscais.
    """
    return render(request, 'users/notas_fiscais.html')


@login_required
def emitir_nfse(request):
    """
    View para emissão de NFS-e.
    """
    return render(request, 'users/nf/emitir_nfse.html')


@login_required
def tutorial_nfse(request):
    """
    View com tutorial de como emitir NF de serviço.
    """
    return render(request, 'users/nf/tutorial_nfse.html')


@login_required
def importar_notas(request):
    """
    View para importar/enviar notas fiscais para a contabilidade.
    """
    from apps.documents.models import NotaFiscal, NotaFiscalCliente
    
    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo_nf')
        descricao = request.POST.get('descricao', '')
        
        if arquivo:
            try:
                NotaFiscalCliente.objects.create(
                    cliente=request.user,
                    arquivo=arquivo,
                    descricao=descricao
                )
                messages.success(request, 'Nota fiscal enviada com sucesso! A equipe de contabilidade será notificada.')
                return redirect('users:importar_notas')
            except Exception as e:
                messages.error(request, f'Erro ao enviar arquivo: {str(e)}')
        else:
            messages.error(request, 'Por favor, selecione um arquivo para enviar.')
    
    # Buscar notas enviadas pelo cliente
    notas_enviadas = NotaFiscalCliente.objects.filter(cliente=request.user).order_by('-data_envio')
    
    context = {
        'notas_enviadas': notas_enviadas,
        'total_enviadas': notas_enviadas.count(),
    }
    
    return render(request, 'users/nf/importar_notas.html', context)


@login_required
def consultar_notas(request):
    """
    View para consultar notas fiscais emitidas e recebidas.
    """
    from apps.documents.models import NotaFiscal, NotaFiscalCliente
    
    notas_recebidas = NotaFiscal.objects.filter(cliente=request.user).order_by('-data_upload')
    notas_enviadas = NotaFiscalCliente.objects.filter(cliente=request.user).order_by('-data_envio')
    
    context = {
        'notas_recebidas': notas_recebidas,
        'notas_enviadas': notas_enviadas,
        'total_recebidas': notas_recebidas.count(),
        'total_enviadas': notas_enviadas.count(),
    }
    
    return render(request, 'users/nf/consultar_notas.html', context)


@login_required
def cancelar_nota(request):
    """
    View para solicitar cancelamento de nota fiscal.
    """
    return render(request, 'users/nf/cancelar_nota.html')


@login_required
def notas_tomadas(request):
    """
    View para registrar notas tomadas (notas de serviços contratados).
    """
    return render(request, 'users/nf/notas_tomadas.html')


@login_required
def minha_aliquota(request):
    """
    View para exibir a alíquota de ISS do cliente.
    """
    return render(request, 'users/nf/minha_aliquota.html')


@login_required
def pendencias(request):
    """View menu para Obrigações (Certidões, Guias, Impostos).
    
    Exibe um menu com links para as subpáginas.
    """
    return render(request, 'users/obrigacoes.html')


@login_required
def certidoes_negativas(request):
    """View para Certidões Negativas.

    Recupera o último envio por tipo para o usuário logado e envia ao template.
    """
    user = request.user
    # Para cada tipo, buscar o último registro (ou None)
    def last_for(tipo_key):
        try:
            return CertidaoNegativa.objects.filter(cliente=user, tipo=tipo_key).latest('data_envio')
        except CertidaoNegativa.DoesNotExist:
            return None

    cert_federal = last_for(CertidaoNegativa.TIPO_FEDERAL)
    cert_estadual = last_for(CertidaoNegativa.TIPO_ESTADUAL)
    cert_trabalhista = last_for(CertidaoNegativa.TIPO_TRABALHISTA)
    cert_fgts = last_for(CertidaoNegativa.TIPO_FGTS)

    context = {
        'cert_federal': cert_federal,
        'cert_estadual': cert_estadual,
        'cert_trabalhista': cert_trabalhista,
        'cert_fgts': cert_fgts,
    }

    return render(request, 'users/certidoes_negativas.html', context)


@login_required
def guias_pagamento(request):
    """View para Guias de Pagamento.
    
    Exibe todas as guias de impostos do usuário.
    """
    user = request.user
    guias = GuiaImposto.objects.filter(cliente=user).order_by('status', 'vencimento')
    
    # Estatísticas
    guias_a_vencer = guias.filter(status='a_vencer').count()
    guias_atrasadas = guias.filter(status='atrasado').count()
    guias_pagas = guias.filter(status='pago').count()
    
    context = {
        'guias': guias,
        'guias_a_vencer': guias_a_vencer,
        'guias_atrasadas': guias_atrasadas,
        'guias_pagas': guias_pagas,
    }
    
    return render(request, 'users/guias_pagamento.html', context)


@login_required
def historico_imposto(request):
    """View para Histórico de Impostos.
    
    Exibe o histórico de todos os impostos do usuário com filtros.
    """
    from django.db.models import Sum
    
    user = request.user
    
    # Filtros
    ano_selecionado = request.GET.get('ano', '')
    tipo_selecionado = request.GET.get('tipo', '')
    
    # Buscar todas as guias
    historico = GuiaImposto.objects.filter(cliente=user).order_by('-vencimento')
    
    # Anos disponíveis para filtro
    anos_disponiveis = historico.dates('vencimento', 'year').values_list('vencimento__year', flat=True)
    anos_disponiveis = sorted(set(anos_disponiveis), reverse=True)
    
    # Tipos de imposto para filtro
    tipos_imposto = GuiaImposto.TIPO_CHOICES
    
    # Aplicar filtros
    if ano_selecionado:
        historico = historico.filter(vencimento__year=int(ano_selecionado))
    if tipo_selecionado:
        historico = historico.filter(tipo=tipo_selecionado)
    
    # Calcular totais
    total_guias = historico.count()
    total_valor = historico.filter(status='pago').aggregate(total=Sum('valor'))['total'] or 0
    
    context = {
        'historico': historico,
        'anos_disponiveis': anos_disponiveis,
        'tipos_imposto': tipos_imposto,
        'ano_selecionado': ano_selecionado,
        'tipo_selecionado': tipo_selecionado,
        'total_guias': total_guias,
        'total_valor': total_valor,
    }
    
    return render(request, 'users/historico_imposto.html', context)


@login_required
def simulador_imposto(request):
    """View para Simulador de Impostos.
    
    Página com calculadora de impostos.
    """
    return render(request, 'users/simulador_imposto.html')


@login_required
def financeiro(request):
    """
    View para o cliente fazer upload e visualizar seus extratos bancários.
    """
    from apps.documents.models import ExtratoBancario
    from apps.documents.forms import ExtratoBancarioUploadForm
    
    # Processar formulário de upload
    if request.method == 'POST':
        form = ExtratoBancarioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            extrato = form.save(commit=False)
            extrato.cliente = request.user
            # Garantir compatibilidade: preencher `mes_ano` com base no período, se não fornecido
            if not getattr(extrato, 'mes_ano', None):
                sd = getattr(extrato, 'start_date', None)
                ed = getattr(extrato, 'end_date', None)
                if sd and ed and sd.year == ed.year and sd.month == ed.month:
                    extrato.mes_ano = sd.strftime('%m/%Y')
                else:
                    # se período cobre mais de um mês, armazenar como 'YYYYMMDD-YYYYMMDD'
                    try:
                        s = sd.strftime('%Y%m%d') if sd else ''
                        e = ed.strftime('%Y%m%d') if ed else ''
                        extrato.mes_ano = f'{s}-{e}'
                    except Exception:
                        extrato.mes_ano = ''
            extrato.save()
            
            messages.success(
                request,
                f'Extrato bancário de {extrato.mes_ano} enviado com sucesso!'
            )
            return redirect('users:financeiro')
    else:
        form = ExtratoBancarioUploadForm()
    
    # Buscar todos os extratos do usuário
    extratos = ExtratoBancario.objects.filter(cliente=request.user).order_by('-data_upload')
    
    context = {
        'form': form,
        'extratos': extratos,
        'total_extratos': extratos.count(),
    }
    
    return render(request, 'users/financeiro.html', context)


@login_required
def minha_empresa(request):
    """
    View para o cliente visualizar os documentos da sua empresa.
    """
    from apps.documents.models import DocumentoEmpresa
    
    # Buscar todos os documentos da empresa do usuário logado
    documentos = DocumentoEmpresa.objects.filter(cliente=request.user).order_by('-data_upload')
    
    # Configuração das fases
    fases = [
        {'id': 'fase_1', 'nome': 'Planejamento', 'descricao': 'Análise Inicial', 'step': 1},
        {'id': 'fase_2', 'nome': 'Viabilidade', 'descricao': 'Consulta Prévia', 'step': 2},
        {'id': 'fase_3', 'nome': 'Registro', 'descricao': 'Contrato Social', 'step': 3},
        {'id': 'fase_4', 'nome': 'Inscrições', 'descricao': 'CNPJ e Inscrições', 'step': 4},
        {'id': 'fase_5', 'nome': 'Licenças', 'descricao': 'Alvarás', 'step': 5},
        {'id': 'fase_6', 'nome': 'Tributário', 'descricao': 'Enquadramento', 'step': 6},
        {'id': 'fase_7', 'nome': 'Concluído', 'descricao': 'Empresa Aberta', 'step': 7},
    ]
    
    fase_atual_id = 'fase_1'
    if hasattr(request.user, 'cliente_profile'):
        fase_atual_id = request.user.cliente_profile.fase_abertura
        
    # Determinar passo atual
    current_step = 1
    for fase in fases:
        if fase['id'] == fase_atual_id:
            current_step = fase['step']
            break
            
    # Definir status de cada fase
    for fase in fases:
        if fase_atual_id == 'fase_7':
            fase['status'] = 'completed'
        elif fase['step'] < current_step:
            fase['status'] = 'completed'
        elif fase['step'] == current_step:
            fase['status'] = 'active'
        else:
            fase['status'] = 'pending'
    
    # Dados da empresa (cliente_profile)
    cliente_profile = None
    if hasattr(request.user, 'cliente_profile'):
        cliente_profile = request.user.cliente_profile
    
    context = {
        'documentos': documentos,
        'total_documentos': documentos.count(),
        'fases': fases,
        'fase_atual_id': fase_atual_id,
        'is_concluido': fase_atual_id == 'fase_7',
        'cliente_profile': cliente_profile,
    }
    
    return render(request, 'users/minha_empresa.html', context)


@login_required
def mensalidade(request):
    """
    View para o cliente visualizar seus boletos de contabilidade.
    Renomeada para exibir apenas boletos da mensalidade.
    """
    from apps.documents.models import BoletoContabilidade
    from datetime import date
    
    # Buscar todos os boletos do usuário logado
    boletos = BoletoContabilidade.objects.filter(cliente=request.user).order_by('-criado_em')
    
    # Atualizar status de vencidos automaticamente
    hoje = date.today()
    boletos_pendentes = boletos.filter(status='pendente', data_vencimento__lt=hoje)
    for boleto in boletos_pendentes:
        boleto.status = 'vencido'
        boleto.save()
    
    # Recarregar boletos após atualização
    boletos = BoletoContabilidade.objects.filter(cliente=request.user).order_by('-criado_em')
    
    # Estatísticas
    total_boletos = boletos.count()
    boletos_pendentes_count = boletos.filter(status='pendente').count()
    boletos_vencidos_count = boletos.filter(status='vencido').count()
    boletos_pagos_count = boletos.filter(status='pago').count()
    
    context = {
        'boletos': boletos,
        'total_boletos': total_boletos,
        'boletos_pendentes': boletos_pendentes_count,
        'boletos_vencidos': boletos_vencidos_count,
        'boletos_pagos': boletos_pagos_count,
    }
    
    return render(request, 'users/mensalidade.html', context)


@login_required
def ver_faturas(request):
    """View para o cliente visualizar suas faturas e boletos."""
    from apps.documents.models import BoletoContabilidade
    from datetime import date
    
    # Buscar todos os boletos do usuário logado
    boletos = BoletoContabilidade.objects.filter(cliente=request.user).order_by('-criado_em')
    
    # Atualizar status de vencidos automaticamente
    hoje = date.today()
    boletos_pendentes = boletos.filter(status='pendente', data_vencimento__lt=hoje)
    for boleto in boletos_pendentes:
        boleto.status = 'vencido'
        boleto.save()
    
    # Recarregar boletos após atualização
    boletos = BoletoContabilidade.objects.filter(cliente=request.user).order_by('-criado_em')
    
    # Estatísticas
    total_boletos = boletos.count()
    boletos_pendentes_count = boletos.filter(status='pendente').count()
    boletos_vencidos_count = boletos.filter(status='vencido').count()
    boletos_pagos_count = boletos.filter(status='pago').count()
    
    context = {
        'boletos': boletos,
        'total_boletos': total_boletos,
        'boletos_pendentes': boletos_pendentes_count,
        'boletos_vencidos': boletos_vencidos_count,
        'boletos_pagos': boletos_pagos_count,
    }
    
    return render(request, 'users/ver_faturas.html', context)


@login_required
def historico_pagamentos(request):
    """View para o cliente consultar histórico de pagamentos."""
    from apps.documents.models import BoletoContabilidade
    
    # Buscar apenas boletos pagos do usuário
    boletos_pagos = BoletoContabilidade.objects.filter(
        cliente=request.user, 
        status='pago'
    ).order_by('-atualizado_em', '-criado_em')
    
    context = {
        'boletos_pagos': boletos_pagos,
        'total_pagos': boletos_pagos.count(),
    }
    
    return render(request, 'users/historico_pagamentos.html', context)


@login_required
def formas_pagamento(request):
    """View para o cliente gerenciar formas de pagamento."""
    context = {}
    return render(request, 'users/formas_pagamento.html', context)


@login_required
def contabilidade(request):
    """Renderiza a página de contabilidade com rascunhos e histórico (padrão)."""
    # Rascunhos do usuário
    drafts = MovimentacaoFinanceira.objects.filter(user=request.user, status=MovimentacaoFinanceira.STATUS_RASCUNHO).order_by('-created_at')

    # Histórico transmitido por padrão (pode ser filtrado via AJAX)
    history_qs = MovimentacaoFinanceira.objects.filter(user=request.user, status__in=[MovimentacaoFinanceira.STATUS_TRANSMITIDO, MovimentacaoFinanceira.STATUS_PROCESSADO, MovimentacaoFinanceira.STATUS_COM_PENDENCIA]).order_by('-competencia')

    context = {
        'drafts': drafts,
        'history': history_qs[:50],  # limit initial
    }
    return render(request, 'users/contabilidade.html', context)


def movimentacao_to_dict(obj):
    return {
        'id': obj.id,
        'tipo': obj.tipo,
        'tipo_display': obj.get_tipo_display(),
        'nome': obj.nome,
        'competencia': obj.competencia.strftime('%Y-%m'),
        'valor': str(obj.valor),
        'anexo_url': obj.anexo.url if obj.anexo else None,
        'status': obj.status,
        'status_display': obj.get_status_display(),
        'created_at': obj.created_at.isoformat(),
    }


@login_required
@require_POST
def add_movimentacao(request):
    """Cria uma movimentação em status Rascunho via AJAX (FormData)."""
    tipo = request.POST.get('tipo')
    nome = request.POST.get('nome')
    competencia_raw = request.POST.get('competencia')  # expected YYYY-MM from <input type="month">
    valor_raw = request.POST.get('valor')

    if not all([tipo, nome, competencia_raw, valor_raw]):
        return JsonResponse({'success': False, 'error': 'Campos obrigatórios faltando.'}, status=400)

    # parse competencia
    try:
        # competência como YYYY-MM -> convert to YYYY-MM-01
        competencia_date = parse_date(competencia_raw + '-01') if len(competencia_raw) == 7 else parse_date(competencia_raw)
    except Exception:
        competencia_date = None

    if not competencia_date:
        return JsonResponse({'success': False, 'error': 'Data de competência inválida.'}, status=400)

    try:
        valor = Decimal(valor_raw.replace(',', '.'))
    except (InvalidOperation, AttributeError):
        return JsonResponse({'success': False, 'error': 'Valor inválido.'}, status=400)

    anexo = request.FILES.get('anexo')

    # validação de anexo
    is_valid, err = validate_file_upload(anexo)
    if not is_valid:
        return JsonResponse({'success': False, 'error': err}, status=400)

    mov = MovimentacaoFinanceira.objects.create(
        user=request.user,
        tipo=tipo,
        nome=nome,
        competencia=competencia_date,
        valor=valor,
        anexo=anexo if anexo else None,
        status=MovimentacaoFinanceira.STATUS_RASCUNHO,
    )

    return JsonResponse({'success': True, 'mov': movimentacao_to_dict(mov)})


@login_required
@require_POST
def edit_movimentacao(request, pk):
    """Edita uma movimentação (somente dono) via AJAX."""
    try:
        mov = MovimentacaoFinanceira.objects.get(pk=pk, user=request.user)
    except MovimentacaoFinanceira.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Movimentação não encontrada.'}, status=404)

    if mov.status != MovimentacaoFinanceira.STATUS_RASCUNHO:
        return JsonResponse({'success': False, 'error': 'Só é possível editar rascunhos.'}, status=400)

    tipo = request.POST.get('tipo')
    nome = request.POST.get('nome')
    competencia_raw = request.POST.get('competencia')
    valor_raw = request.POST.get('valor')

    if not all([tipo, nome, competencia_raw, valor_raw]):
        return JsonResponse({'success': False, 'error': 'Campos obrigatórios faltando.'}, status=400)

    try:
        competencia_date = parse_date(competencia_raw + '-01') if len(competencia_raw) == 7 else parse_date(competencia_raw)
    except Exception:
        competencia_date = None
    if not competencia_date:
        return JsonResponse({'success': False, 'error': 'Data de competência inválida.'}, status=400)

    try:
        valor = Decimal(valor_raw.replace(',', '.'))
    except (InvalidOperation, AttributeError):
        return JsonResponse({'success': False, 'error': 'Valor inválido.'}, status=400)

    # Atualizar campos
    mov.tipo = tipo
    mov.nome = nome
    mov.competencia = competencia_date
    mov.valor = valor
    if 'anexo' in request.FILES:
        anexo_new = request.FILES.get('anexo')
        is_valid, err = validate_file_upload(anexo_new)
        if not is_valid:
            return JsonResponse({'success': False, 'error': err}, status=400)
        mov.anexo = anexo_new
    mov.save()

    return JsonResponse({'success': True, 'mov': movimentacao_to_dict(mov)})


@login_required
@require_POST
def delete_movimentacao(request, pk):
    try:
        mov = MovimentacaoFinanceira.objects.get(pk=pk, user=request.user)
    except MovimentacaoFinanceira.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Movimentação não encontrada.'}, status=404)

    if mov.status != MovimentacaoFinanceira.STATUS_RASCUNHO:
        return JsonResponse({'success': False, 'error': 'Só é possível excluir rascunhos.'}, status=400)

    mov.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def transmit_movimentacoes(request):
    """Marca rascunhos como transmitidos. Se `month` (YYYY-MM) for fornecido, transmite apenas para esse mês.
    Cria ou reutiliza uma TransmissaoMensal para agrupar os lançamentos.
    """
    month = request.POST.get('month')
    if month and len(month) == 7:
        try:
            comp = parse_date(month + '-01')
        except Exception:
            return JsonResponse({'success': False, 'error': 'Mês inválido.'}, status=400)
        drafts = MovimentacaoFinanceira.objects.filter(user=request.user, status=MovimentacaoFinanceira.STATUS_RASCUNHO, competencia__year=comp.year, competencia__month=comp.month)
    else:
        drafts = MovimentacaoFinanceira.objects.filter(user=request.user, status=MovimentacaoFinanceira.STATUS_RASCUNHO)

    count = drafts.count()
    if count == 0:
        return JsonResponse({'success': True, 'transmitted': 0})

    # Cria/transmissao mensal
    comp_date = drafts.first().competencia.replace(day=1)
    transmissao, created = TransmissaoMensal.objects.get_or_create(user=request.user, competencia=comp_date)

    # Atualiza movimentos
    drafts.update(status=MovimentacaoFinanceira.STATUS_TRANSMITIDO, transmissao=transmissao, updated_at=timezone.now())
    return JsonResponse({'success': True, 'transmitted': count, 'transmissao_id': transmissao.id})


@login_required
def drafts_by_month(request):
    """Retorna rascunhos para o mês selecionado e os totais por tipo."""
    month = request.GET.get('month')
    if not month or len(month) != 7:
        return JsonResponse({'success': False, 'error': 'Mês inválido.'}, status=400)
    try:
        comp = parse_date(month + '-01')
    except Exception:
        return JsonResponse({'success': False, 'error': 'Mês inválido.'}, status=400)

    drafts = MovimentacaoFinanceira.objects.filter(user=request.user, status=MovimentacaoFinanceira.STATUS_RASCUNHO, competencia__year=comp.year, competencia__month=comp.month).order_by('-created_at')

    total_receitas = drafts.filter(tipo='receita').aggregate(total=Sum('valor'))['total'] or 0
    total_despesas = drafts.filter(tipo='despesa').aggregate(total=Sum('valor'))['total'] or 0

    items = [movimentacao_to_dict(m) for m in drafts]
    return JsonResponse({'success': True, 'items': items, 'totals': {'receitas': str(total_receitas), 'despesas': str(total_despesas)}})


@login_required
def months_transmitted(request):
    """Lista os meses que já foram transmitidos pelo usuário."""
    transmissoes = TransmissaoMensal.objects.filter(user=request.user).order_by('-competencia')
    items = []
    for t in transmissoes:
        items.append({
            'id': t.id,
            'competencia': t.competencia.strftime('%Y-%m'),
            'transmitted_at': t.transmitted_at.isoformat(),
            'count': t.movimentacoes.count(),
        })
    return JsonResponse({'success': True, 'items': items})


@login_required
def transmitted_month_detail(request, pk):
    """Detalhe (read-only) das movimentações de uma TransmissaoMensal (acessível ao dono)."""
    try:
        t = TransmissaoMensal.objects.get(pk=pk, user=request.user)
    except TransmissaoMensal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Transmissão não encontrada.'}, status=404)

    items = [movimentacao_to_dict(m) for m in t.movimentacoes.order_by('-competencia')]
    return JsonResponse({'success': True, 'transmissao': {'id': t.id, 'competencia': t.competencia.strftime('%Y-%m'), 'transmitted_at': t.transmitted_at.isoformat()}, 'items': items})


@login_required
def contabilidade_history(request):
    """Retorna histórico filtrado por mês/ano (AJAX GET)."""
    month = request.GET.get('month')  # 'YYYY-MM'
    qs = MovimentacaoFinanceira.objects.filter(user=request.user, status__in=[MovimentacaoFinanceira.STATUS_TRANSMITIDO, MovimentacaoFinanceira.STATUS_PROCESSADO, MovimentacaoFinanceira.STATUS_COM_PENDENCIA])
    if month and len(month) == 7:
        try:
            comp = parse_date(month + '-01')
            qs = qs.filter(competencia__year=comp.year, competencia__month=comp.month)
        except Exception:
            pass

    items = [movimentacao_to_dict(m) for m in qs.order_by('-competencia')[:200]]
    return JsonResponse({'success': True, 'items': items})


@login_required
def meu_plano(request):
    """View para Meu Plano - exibe informações da assinatura do usuário"""
    from apps.services.models import Subscription, Plano
    
    # Buscar assinatura ativa do usuário
    subscription = Subscription.objects.filter(
        cliente=request.user, 
        status='ativa'
    ).select_related('plano').first()
    
    # Se não tiver ativa, busca a última assinatura
    if not subscription:
        subscription = Subscription.objects.filter(
            cliente=request.user
        ).select_related('plano').order_by('-criado_em').first()
    
    # Buscar o plano correspondente no modelo Plano (marketing) para obter features
    plano_marketing = None
    if subscription and subscription.plano:
        # Buscar planos com o mesmo nome que tenham features configuradas
        planos_candidatos = Plano.objects.filter(
            nome__iexact=subscription.plano.nome
        )
        # Preferir o plano que tem features preenchidas
        for p in planos_candidatos:
            if p.features_included or p.features_excluded:
                plano_marketing = p
                break
        # Se nenhum tem features, pega o primeiro
        if not plano_marketing:
            plano_marketing = planos_candidatos.first()
    
    context = {
        'subscription': subscription,
        'plano_marketing': plano_marketing,
    }
    
    return render(request, 'users/meu_plano.html', context)


@login_required
def servicos_avulsos(request):
    """View para Serviços Avulsos - Lista serviços disponíveis e contratações do usuário"""
    from apps.services.models import ServicoAvulso, ContratacaoServicoAvulso
    
    # Serviços ativos disponíveis
    servicos = ServicoAvulso.objects.filter(ativo=True).order_by('ordem', 'titulo')
    
    # Contratações do usuário
    minhas_contratacoes = ContratacaoServicoAvulso.objects.filter(
        usuario=request.user
    ).select_related('servico').order_by('-criado_em')
    
    context = {
        'servicos': servicos,
        'minhas_contratacoes': minhas_contratacoes,
    }
    return render(request, 'users/servicos_avulsos.html', context)


@login_required
@require_POST
def contratar_servico_avulso(request, servico_id):
    """View para contratar um serviço avulso"""
    from apps.services.models import ServicoAvulso, ContratacaoServicoAvulso
    
    try:
        servico = ServicoAvulso.objects.get(id=servico_id, ativo=True)
    except ServicoAvulso.DoesNotExist:
        messages.error(request, 'Serviço não encontrado ou não está mais disponível.')
        return redirect('users:servicos_avulsos')
    
    observacoes = request.POST.get('observacoes', '').strip()
    
    # Criar a contratação
    contratacao = ContratacaoServicoAvulso.objects.create(
        usuario=request.user,
        servico=servico,
        valor_contratado=servico.valor,
        observacoes_cliente=observacoes if observacoes else None,
        status='pendente'
    )
    
    messages.success(
        request, 
        f'Serviço "{servico.titulo}" contratado com sucesso! Nossa equipe entrará em contato em breve.'
    )
    return redirect('users:servicos_avulsos')


@login_required
def minhas_contratacoes_avulsas(request):
    """API que retorna as contratações do usuário em JSON"""
    from apps.services.models import ContratacaoServicoAvulso
    
    contratacoes = ContratacaoServicoAvulso.objects.filter(
        usuario=request.user
    ).select_related('servico').order_by('-criado_em')
    
    data = []
    for c in contratacoes:
        data.append({
            'id': c.id,
            'servico': c.servico.titulo,
            'valor': float(c.valor_contratado),
            'status': c.status,
            'status_display': c.get_status_display(),
            'criado_em': c.criado_em.strftime('%d/%m/%Y %H:%M'),
            'concluido_em': c.concluido_em.strftime('%d/%m/%Y %H:%M') if c.concluido_em else None,
        })
    
    return JsonResponse({'success': True, 'contratacoes': data})


@login_required
def indique_ganhe(request):
    """View para Indique e Ganhe"""
    return render(request, 'users/indique_ganhe.html')


@login_required
def meu_perfil(request):
    """View para visualizar e editar o perfil do usuário"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            cpf_cnpj = request.POST.get('cpf_cnpj')
            
            # Validações básicas
            if not first_name or not email:
                messages.error(request, 'Nome e e-mail são obrigatórios.')
                return redirect('users:meu_perfil')
            
            # Verificar se e-mail já existe (se foi alterado)
            if email != request.user.email and User.objects.filter(email=email).exists():
                messages.error(request, 'Este e-mail já está sendo utilizado por outro usuário.')
                return redirect('users:meu_perfil')
                
            try:
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.email = email
                # Se o username for o email, atualiza também
                if '@' in request.user.username: 
                    request.user.username = email
                
                request.user.telefone = telefone
                request.user.cpf_cnpj = cpf_cnpj
                request.user.save()
                
                messages.success(request, 'Dados pessoais atualizados com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar perfil: {str(e)}')
                
        elif action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not request.user.check_password(current_password):
                messages.error(request, 'A senha atual está incorreta.')
            elif new_password != confirm_password:
                messages.error(request, 'A nova senha e a confirmação não coincidem.')
            elif len(new_password) < 6:
                messages.error(request, 'A nova senha deve ter pelo menos 6 caracteres.')
            else:
                request.user.set_password(new_password)
                request.user.save()
                login(request, request.user) # Manter usuário logado após mudar senha
                messages.success(request, 'Senha alterada com sucesso!')
        
        return redirect('users:meu_perfil')
        
    return render(request, 'users/meu_perfil.html')


def forgot_password_view(request):
    """View para solicitar recuperação de senha"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Gerar código de 6 dígitos
            code = str(random.randint(100000, 999999))
            
            # Salvar na sessão
            request.session['reset_code'] = code
            request.session['reset_email'] = email
            request.session.set_expiry(600)  # Expira em 10 minutos
            
            # Enviar e-mail (usando configuração existente)
            subject = 'Seu código de verificação - Vetorial'
            message = f'Olá, {user.first_name}.\n\nSeu código de verificação para redefinir a senha é: {code}\n\nEste código expira em 10 minutos.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            messages.success(request, 'Código de verificação enviado para seu e-mail.')
            return redirect('users:verify_code')
            
        except User.DoesNotExist:
            # Por segurança, não informamos se o e-mail não existe, mas neste caso
            # para UX vamos informar ou fingir que enviou.
            # Vamos informar erro para facilitar.
            messages.error(request, 'E-mail não encontrado.')
    
    return render(request, 'users/forgot_password.html')


def verify_code_view(request):
    """View para verificar o código de 6 dígitos"""
    if 'reset_code' not in request.session:
        messages.error(request, 'Sessão expirada. Solicite um novo código.')
        return redirect('users:forgot_password')
        
    if request.method == 'POST':
        code = request.POST.get('code')
        session_code = request.session.get('reset_code')
        
        if code == session_code:
            request.session['reset_verified'] = True
            return redirect('users:reset_password')
        else:
            messages.error(request, 'Código inválido. Tente novamente.')
            
    return render(request, 'users/verify_code.html')


def reset_password_view(request):
    """View para definir a nova senha"""
    if not request.session.get('reset_verified'):
        messages.error(request, 'Acesso não autorizado.')
        return redirect('users:login')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'As senhas não conferem.')
        else:
            email = request.session.get('reset_email')
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                
                # Limpar sessão
                del request.session['reset_code']
                del request.session['reset_email']
                del request.session['reset_verified']
                
                messages.success(request, 'Senha alterada com sucesso! Faça login.')
                return redirect('users:login')
                
            except User.DoesNotExist:
                messages.error(request, 'Erro ao localizar usuário.')
                
    return render(request, 'users/reset_password.html')
