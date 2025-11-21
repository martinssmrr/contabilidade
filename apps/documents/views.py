from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import NotaFiscal, DocumentoEmpresa
from .forms import NotaFiscalUploadForm, DocumentoEmpresaUploadForm

User = get_user_model()


@staff_member_required
def client_list_view(request):
    """
    View para listar todos os clientes (usuários não-staff).
    Acessível apenas para membros da equipe.
    """
    # Busca todos os usuários que não são staff
    clientes = User.objects.filter(is_staff=False).order_by('first_name', 'last_name', 'username')
    
    # Filtro de busca opcional
    search_query = request.GET.get('search', '')
    if search_query:
        clientes = clientes.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    context = {
        'clientes': clientes,
        'search_query': search_query,
        'total_clientes': clientes.count(),
    }
    
    return render(request, 'documents/staff/client_list.html', context)


@staff_member_required
def client_detail_view(request, pk):
    """
    View para exibir detalhes do cliente e gerenciar suas notas fiscais e documentos da empresa.
    Permite upload de novas notas fiscais e documentos.
    """
    cliente = get_object_or_404(User, pk=pk, is_staff=False)
    
    # Identificar qual formulário foi enviado
    form_type = request.POST.get('form_type', '')
    
    # Processar formulários de upload
    if request.method == 'POST':
        if form_type == 'nota_fiscal':
            form_nf = NotaFiscalUploadForm(request.POST, request.FILES)
            if form_nf.is_valid():
                nota_fiscal = form_nf.save(commit=False)
                nota_fiscal.cliente = cliente
                nota_fiscal.enviado_por = request.user
                nota_fiscal.save()
                
                messages.success(
                    request,
                    f'Nota fiscal enviada com sucesso para {cliente.get_full_name() or cliente.username}!'
                )
                return redirect('documents:client_detail', pk=cliente.pk)
            form_doc = DocumentoEmpresaUploadForm()
        
        elif form_type == 'documento_empresa':
            form_doc = DocumentoEmpresaUploadForm(request.POST, request.FILES)
            if form_doc.is_valid():
                documento = form_doc.save(commit=False)
                documento.cliente = cliente
                documento.enviado_por = request.user
                documento.save()
                
                messages.success(
                    request,
                    f'Documento "{documento.titulo}" enviado com sucesso para {cliente.get_full_name() or cliente.username}!'
                )
                return redirect('documents:client_detail', pk=cliente.pk)
            form_nf = NotaFiscalUploadForm()
        else:
            form_nf = NotaFiscalUploadForm()
            form_doc = DocumentoEmpresaUploadForm()
    else:
        form_nf = NotaFiscalUploadForm()
        form_doc = DocumentoEmpresaUploadForm()
    
    # Buscar todas as notas fiscais e documentos do cliente
    notas_fiscais = NotaFiscal.objects.filter(cliente=cliente).order_by('-data_upload')
    documentos_empresa = DocumentoEmpresa.objects.filter(cliente=cliente).order_by('-data_upload')
    
    context = {
        'cliente': cliente,
        'form_nf': form_nf,
        'form_doc': form_doc,
        'notas_fiscais': notas_fiscais,
        'documentos_empresa': documentos_empresa,
        'total_notas': notas_fiscais.count(),
        'total_documentos': documentos_empresa.count(),
    }
    
    return render(request, 'documents/staff/client_detail.html', context)


@login_required
def minhas_notas_fiscais_view(request):
    """
    View para o cliente visualizar suas próprias notas fiscais.
    Acessível apenas para usuários autenticados (clientes).
    """
    # Buscar todas as notas fiscais do usuário logado
    notas_fiscais = NotaFiscal.objects.filter(cliente=request.user).order_by('-data_upload')
    
    context = {
        'notas_fiscais': notas_fiscais,
        'total_notas': notas_fiscais.count(),
    }
    
    return render(request, 'documents/minhas_notas_fiscais.html', context)
