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

from .models import MovimentacaoFinanceira
from .models import TransmissaoMensal
from .models import CertidaoNegativa
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
    View para o cliente visualizar e enviar notas fiscais.
    """
    from apps.documents.models import NotaFiscal, NotaFiscalCliente
    
    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo_nf')
        descricao = request.POST.get('descricao', '')
        
        if arquivo:
            # Validar tamanho/extensão se necessário (usando utils existente se houver)
            # from .utils import validate_file_upload
            # is_valid, err = validate_file_upload(arquivo)
            # if not is_valid: messages.error...
            
            try:
                NotaFiscalCliente.objects.create(
                    cliente=request.user,
                    arquivo=arquivo,
                    descricao=descricao
                )
                messages.success(request, 'Nota fiscal enviada com sucesso! A equipe de contabilidade será notificada.')
                return redirect('users:notas_fiscais')
            except Exception as e:
                messages.error(request, f'Erro ao enviar arquivo: {str(e)}')
        else:
            messages.error(request, 'Por favor, selecione um arquivo para enviar.')
            
    # Buscar todas as notas fiscais do usuário logado (Recebidas)
    notas_recebidas = NotaFiscal.objects.filter(cliente=request.user).order_by('-data_upload')
    
    # Buscar notas enviadas pelo cliente
    notas_enviadas = NotaFiscalCliente.objects.filter(cliente=request.user).order_by('-data_envio')
    
    context = {
        'notas_fiscais': notas_recebidas, # Manter compatibilidade se o template antigo for usado temporariamente
        'notas_recebidas': notas_recebidas,
        'notas_enviadas': notas_enviadas,
        'total_notas': notas_recebidas.count(),
        'total_recebidas': notas_recebidas.count(),
        'total_enviadas': notas_enviadas.count(),
    }
    
    return render(request, 'users/notas_fiscais.html', context)


@login_required
def pendencias(request):
    """View para Certidões Negativas (pendências).

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

    return render(request, 'users/pendencias.html', context)


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
    
    context = {
        'documentos': documentos,
        'total_documentos': documentos.count(),
        'fases': fases,
        'fase_atual_id': fase_atual_id,
        'is_concluido': fase_atual_id == 'fase_7'
    }
    
    return render(request, 'users/minha_empresa.html', context)


@login_required
def documentos(request):
    """
    View para o cliente visualizar todos os seus documentos.
    Inclui: Notas Fiscais e Documentos da Empresa.
    """
    from apps.documents.models import NotaFiscal, DocumentoEmpresa
    
    # Buscar todos os documentos do usuário logado
    notas_fiscais = NotaFiscal.objects.filter(cliente=request.user).order_by('-data_upload')
    documentos_empresa = DocumentoEmpresa.objects.filter(cliente=request.user).order_by('-data_upload')
    
    context = {
        'notas_fiscais': notas_fiscais,
        'documentos_empresa': documentos_empresa,
        'total_notas': notas_fiscais.count(),
        'total_documentos': documentos_empresa.count(),
        'total_geral': notas_fiscais.count() + documentos_empresa.count(),
    }
    
    return render(request, 'users/documentos.html', context)


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
    """View para Meu Plano"""
    return render(request, 'users/meu_plano.html')


@login_required
def servicos_avulsos(request):
    """View para Serviços Avulsos"""
    return render(request, 'users/servicos_avulsos.html')


@login_required
def indique_ganhe(request):
    """View para Indique e Ganhe"""
    return render(request, 'users/indique_ganhe.html')
