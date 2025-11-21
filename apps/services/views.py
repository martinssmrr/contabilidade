from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import ProcessoAbertura, Socio
from .forms import (
    Etapa1DadosPessoaisForm, Etapa2EnderecoForm, Etapa3DadosEmpresaForm,
    SocioFormSet, Etapa5DocumentosForm, Etapa6InformacoesFiscaisForm,
    Etapa7DadosAcessoForm, Etapa8AssinaturaForm, Etapa9PagamentoForm
)


@login_required
def abertura_empresa_wizard(request, etapa=1):
    """
    View principal do wizard de abertura de empresa
    Gerencia todas as 9 etapas do processo
    """
    from .models import Plano
    
    # Busca ou cria um processo em andamento para o usuário
    processo, created = ProcessoAbertura.objects.get_or_create(
        usuario=request.user,
        status__in=['rascunho', 'em_andamento'],
        defaults={'etapa_atual': 1, 'status': 'em_andamento'}
    )
    
    # Validar se a etapa solicitada é válida
    if etapa < 1 or etapa > 9:
        messages.error(request, 'Etapa inválida.')
        return redirect('services:abertura_empresa', etapa=1)
    
    # Não permitir pular etapas
    if etapa > processo.etapa_atual + 1:
        messages.warning(request, 'Por favor, complete as etapas anteriores primeiro.')
        return redirect('services:abertura_empresa', etapa=processo.etapa_atual)
    
    # Selecionar o formulário da etapa atual
    form_class = get_form_for_etapa(etapa)
    
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
            form = form_class(request.POST, request.FILES, instance=processo)
            if form.is_valid():
                form.save()
                
                # Atualizar etapa
                if etapa >= processo.etapa_atual:
                    processo.etapa_atual = etapa + 1
                
                # Etapa 8: registrar data de assinatura
                if etapa == 8:
                    processo.data_assinatura = timezone.now()
                
                # Etapa 9: marcar como aguardando pagamento
                if etapa == 9:
                    processo.status = 'aguardando_pagamento'
                
                processo.save()
                
                if etapa < 9:
                    messages.success(request, f'Etapa {etapa} concluída com sucesso!')
                    return redirect('services:abertura_empresa', etapa=etapa + 1)
                else:
                    messages.success(request, 'Processo de abertura concluído! Prossiga para o pagamento.')
                    return redirect('services:pagamento_abertura', processo_id=processo.id)
    
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
        else:
            form = form_class(instance=processo)
            formset = None
    
    # Calcular progresso
    progresso = (etapa / 9) * 100
    
    # Buscar planos disponíveis para a etapa 9 (filtrados por tipo de atividade)
    planos_abertura = None
    if etapa == 9:
        # Mapear tipo_atividade para categoria de plano
        tipo_atividade = processo.tipo_atividade
        
        # Definir categoria baseada no tipo de atividade escolhido na etapa 6
        if tipo_atividade == 'servico':
            categoria_plano = 'servicos'
        elif tipo_atividade == 'comercio':
            categoria_plano = 'comercio'
        else:
            # Fallback: Se não houver tipo_atividade ou for 'industria'/'misto', mostrar planos de abertura
            categoria_plano = 'abertura'
        
        planos_abertura = Plano.objects.filter(ativo=True, categoria=categoria_plano).order_by('ordem', 'preco')
    
    context = {
        'processo': processo,
        'etapa': etapa,
        'form': form,
        'formset': formset,
        'progresso': progresso,
        'total_etapas': 9,
        'planos_abertura': planos_abertura,
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
        7: Etapa7DadosAcessoForm,
        8: Etapa8AssinaturaForm,
        9: Etapa9PagamentoForm,
    }
    return forms_map.get(etapa)


@login_required
def pagamento_abertura(request, processo_id):
    """View para processar o pagamento do processo de abertura"""
    processo = get_object_or_404(ProcessoAbertura, id=processo_id, usuario=request.user)
    
    if not processo.plano_selecionado:
        messages.error(request, 'Nenhum plano foi selecionado.')
        return redirect('services:abertura_empresa', etapa=9)
    
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
