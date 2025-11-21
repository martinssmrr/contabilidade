from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

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
        
        if len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
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
@login_required
def notas_fiscais(request):
    """
    View para o cliente visualizar suas próprias notas fiscais.
    """
    from apps.documents.models import NotaFiscal
    
    # Buscar todas as notas fiscais do usuário logado
    notas_fiscais_list = NotaFiscal.objects.filter(cliente=request.user).order_by('-data_upload')
    
    context = {
        'notas_fiscais': notas_fiscais_list,
        'total_notas': notas_fiscais_list.count(),
    }
    
    return render(request, 'users/notas_fiscais.html', context)


@login_required
def pendencias(request):
    """View para Pendências"""
    return render(request, 'users/pendencias.html')


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
@login_required
def minha_empresa(request):
    """
    View para o cliente visualizar os documentos da sua empresa.
    """
    from apps.documents.models import DocumentoEmpresa
    
    # Buscar todos os documentos da empresa do usuário logado
    documentos = DocumentoEmpresa.objects.filter(cliente=request.user).order_by('-data_upload')
    
    context = {
        'documentos': documentos,
        'total_documentos': documentos.count(),
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
    """View para Contabilidade"""
    return render(request, 'users/contabilidade.html')


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
