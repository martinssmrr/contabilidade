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
    View para consulta de CNAEs organizados por categoria
    """
    from .models import CategoriaCNAE
    
    # Buscar todas as categorias com seus CNAEs
    categorias = CategoriaCNAE.objects.prefetch_related('cnaes').all()
    
    # Organizar dados em dicionário para o template
    categorias_com_cnaes = {}
    for categoria in categorias:
        cnaes_ativos = categoria.cnaes.filter(ativo=True)
        if cnaes_ativos.exists():  # Só incluir categorias com CNAEs ativos
            categorias_com_cnaes[categoria] = list(cnaes_ativos)
    
    context = {
        'categorias_com_cnaes': categorias_com_cnaes,
        'total_categorias': len(categorias_com_cnaes),
        'total_cnaes': sum(len(cnaes) for cnaes in categorias_com_cnaes.values()),
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
