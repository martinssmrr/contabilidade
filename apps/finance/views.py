from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from .models import Transaction, Subcategory, Account, ScheduledTransaction
from .forms import TransactionForm, SubcategoryForm, AccountForm, ScheduledTransactionForm
from apps.users.models import MovimentacaoFinanceira

@login_required
def dashboard(request):
    # Filtros de Data
    today = timezone.now().date()
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = today.replace(day=1) # Primeiro dia do mês atual
        
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        # Último dia do mês atual
        next_month = today.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)

    # Filtros Adicionais
    filter_type = request.GET.get('type') # entrada, saida
    filter_subcategory = request.GET.get('subcategory')
    filter_account = request.GET.get('account')

    # Queryset Base
    transactions = Transaction.objects.filter(user=request.user, date__range=[start_date, end_date])

    if filter_type:
        transactions = transactions.filter(account__subcategory__type=filter_type)
    
    if filter_subcategory:
        transactions = transactions.filter(account__subcategory_id=filter_subcategory)
        
    if filter_account:
        transactions = transactions.filter(account_id=filter_account)

    # Totais
    total_entradas = transactions.filter(account__subcategory__type='entrada').aggregate(Sum('value'))['value__sum'] or 0
    total_saidas = transactions.filter(account__subcategory__type='saida').aggregate(Sum('value'))['value__sum'] or 0
    saldo = total_entradas - total_saidas

    # Gráfico (Saídas por Subcategoria)
    saidas_por_subcategoria = []
    if total_saidas > 0:
        subcategories = Subcategory.objects.filter(user=request.user, type='saida')
        for sub in subcategories:
            val = transactions.filter(account__subcategory=sub).aggregate(Sum('value'))['value__sum'] or 0
            if val > 0:
                saidas_por_subcategoria.append({
                    'name': sub.name,
                    'value': float(val)
                })

    # Forms
    transaction_form = TransactionForm(user=request.user)
    subcategory_form = SubcategoryForm()
    account_form = AccountForm(user=request.user)
    
    # Forms para Contas Agendadas
    scheduled_form_entrada = ScheduledTransactionForm(user=request.user, initial={'type': 'entrada'})
    scheduled_form_saida = ScheduledTransactionForm(user=request.user, initial={'type': 'saida'})

    # Contexto para filtros
    user_subcategories = Subcategory.objects.filter(user=request.user)
    user_accounts = Account.objects.filter(user=request.user)

    context = {
        'transactions': transactions,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo': saldo,
        'saidas_por_subcategoria': saidas_por_subcategoria,
        'transaction_form': transaction_form,
        'subcategory_form': subcategory_form,
        'account_form': account_form,
        'scheduled_form_entrada': scheduled_form_entrada,
        'scheduled_form_saida': scheduled_form_saida,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'filter_type': filter_type,
        'filter_subcategory': int(filter_subcategory) if filter_subcategory else '',
        'filter_account': int(filter_account) if filter_account else '',
        'user_subcategories': user_subcategories,
        'user_accounts': user_accounts,
    }
    
    return render(request, 'finance/dashboard.html', context)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Lançamento adicionado com sucesso!')
        else:
            messages.error(request, 'Erro ao adicionar lançamento. Verifique os dados.')
    return redirect('finance:dashboard')

@login_required
def add_subcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.user = request.user
            subcategory.save()
            messages.success(request, 'Subcategoria adicionada com sucesso!')
        else:
            messages.error(request, 'Erro ao adicionar subcategoria.')
    return redirect('finance:dashboard')

@login_required
def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.user, request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Conta adicionada com sucesso!')
        else:
            messages.error(request, 'Erro ao adicionar conta.')
    return redirect('finance:dashboard')

@login_required
def transmit_transactions(request):
    if request.method == 'POST':
        pending_transactions = Transaction.objects.filter(user=request.user, status=Transaction.STATUS_PENDING)
        
        # Criar MovimentacaoFinanceira para cada Transaction
        movimentacoes = []
        for transaction in pending_transactions:
            tipo_mov = 'receita' if transaction.account.subcategory.type == 'entrada' else 'despesa'
            # Usar descrição se houver, senão usar Categoria - Conta
            nome = transaction.description if transaction.description else f"{transaction.account.subcategory.name} - {transaction.account.name}"
            
            movimentacoes.append(MovimentacaoFinanceira(
                user=request.user,
                tipo=tipo_mov,
                nome=nome,
                competencia=transaction.date,
                valor=transaction.value,
                status=MovimentacaoFinanceira.STATUS_TRANSMITIDO
            ))
        
        if movimentacoes:
            MovimentacaoFinanceira.objects.bulk_create(movimentacoes)
            
        count = pending_transactions.count()
        pending_transactions.update(status=Transaction.STATUS_TRANSMITTED)
        
        messages.success(request, f'{count} lançamentos transmitidos para a contabilidade com sucesso!')
    return redirect('finance:dashboard')

@login_required
def get_accounts_ajax(request):
    subcategory_id = request.GET.get('subcategory_id')
    accounts = Account.objects.filter(user=request.user, subcategory_id=subcategory_id).values('id', 'name')
    return JsonResponse(list(accounts), safe=False)

@login_required
def manage_accounts(request):
    subcategories = Subcategory.objects.filter(user=request.user).order_by('type', 'name').prefetch_related('accounts')
    return render(request, 'finance/manage_accounts.html', {'subcategories': subcategories})

@login_required
def delete_subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk, user=request.user)
    if request.method == 'POST':
        subcategory.delete()
        messages.success(request, 'Subcategoria excluída com sucesso!')
    return redirect('finance:manage_accounts')

@login_required
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Conta excluída com sucesso!')
    return redirect('finance:manage_accounts')

@login_required
def edit_subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subcategoria atualizada com sucesso!')
            return redirect('finance:manage_accounts')
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'finance/form.html', {'form': form, 'title': 'Editar Subcategoria'})

@login_required
def edit_account(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.user, request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta atualizada com sucesso!')
            return redirect('finance:manage_accounts')
    else:
        form = AccountForm(request.user, instance=account)
    return render(request, 'finance/form.html', {'form': form, 'title': 'Editar Conta'})

@login_required
def new_subcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.user = request.user
            subcategory.save()
            messages.success(request, 'Subcategoria criada com sucesso!')
            return redirect('finance:manage_accounts')
    else:
        form = SubcategoryForm()
    return render(request, 'finance/form.html', {'form': form, 'title': 'Nova Subcategoria'})

@login_required
def new_account(request):
    if request.method == 'POST':
        form = AccountForm(request.user, request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('finance:manage_accounts')
    else:
        form = AccountForm(request.user)
    return render(request, 'finance/form.html', {'form': form, 'title': 'Nova Conta'})

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lançamento atualizado com sucesso!')
            return redirect('finance:dashboard')
    else:
        form = TransactionForm(request.user, instance=transaction)
    return render(request, 'finance/form.html', {'form': form, 'title': 'Editar Lançamento'})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Lançamento excluído com sucesso!')
    return redirect('finance:dashboard')

@login_required
def generate_report_pdf(request):
    # Filtros (mesma lógica do dashboard)
    today = timezone.now().date()
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = today.replace(day=1)
        
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        next_month = today.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)

    filter_type = request.GET.get('type')
    filter_subcategory = request.GET.get('subcategory')
    filter_account = request.GET.get('account')

    transactions = Transaction.objects.filter(user=request.user, date__range=[start_date, end_date]).order_by('date')

    if filter_type:
        transactions = transactions.filter(account__subcategory__type=filter_type)
    
    if filter_subcategory:
        transactions = transactions.filter(account__subcategory_id=filter_subcategory)
        
    if filter_account:
        transactions = transactions.filter(account_id=filter_account)

    # Totais
    total_entradas = transactions.filter(account__subcategory__type='entrada').aggregate(Sum('value'))['value__sum'] or 0
    total_saidas = transactions.filter(account__subcategory__type='saida').aggregate(Sum('value'))['value__sum'] or 0
    saldo = total_entradas - total_saidas

    # Gerar PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"relatorio_financeiro_{start_date.strftime('%d-%m-%Y')}_{end_date.strftime('%d-%m-%Y')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1 # Center
    )
    elements.append(Paragraph(f"Relatório Financeiro - Vetorial", title_style))
    elements.append(Paragraph(f"Período: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Resumo
    summary_data = [
        ['Resumo do Período', ''],
        ['Total Entradas:', f"R$ {total_entradas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')],
        ['Total Saídas:', f"R$ {total_saidas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')],
        ['Saldo Final:', f"R$ {saldo:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')]
    ]
    
    summary_table = Table(summary_data, colWidths=[4*cm, 4*cm], hAlign='LEFT')
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('TEXTCOLOR', (1, 3), (1, 3), colors.blue if saldo >= 0 else colors.red), # Saldo color
        ('FONTNAME', (0, 3), (1, 3), 'Helvetica-Bold'),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 30))

    # Tabela de Lançamentos
    data = [['Data', 'Tipo', 'Categoria/Conta', 'Descrição', 'Valor']]
    
    for t in transactions:
        tipo = "Entrada" if t.account.subcategory.type == 'entrada' else "Saída"
        valor_str = f"R$ {t.value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        
        # Formatar descrição
        desc = t.description if t.description else "-"
        if len(desc) > 30:
            desc = desc[:27] + "..."
            
        categoria = f"{t.account.subcategory.name}\n{t.account.name}"
        
        data.append([
            t.date.strftime('%d/%m/%Y'),
            tipo,
            categoria,
            desc,
            valor_str
        ])

    # Estilo da tabela
    table = Table(data, colWidths=[2.5*cm, 2*cm, 5*cm, 5*cm, 2.5*cm])
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    
    # Colorir linhas de entrada/saída
    for i, row in enumerate(data[1:], start=1):
        if row[1] == 'Entrada':
            style.add('TEXTCOLOR', (4, i), (4, i), colors.green)
        else:
            style.add('TEXTCOLOR', (4, i), (4, i), colors.red)
            
    table.setStyle(style)
    elements.append(table)

    doc.build(elements)
    return response

@login_required
def add_scheduled_transaction(request):
    if request.method == 'POST':
        form = ScheduledTransactionForm(request.user, request.POST)
        if form.is_valid():
            scheduled = form.save(commit=False)
            scheduled.user = request.user
            scheduled.save()
            messages.success(request, 'Conta agendada com sucesso!')
        else:
            messages.error(request, 'Erro ao agendar conta. Verifique os dados.')
    return redirect('finance:dashboard')

@login_required
def list_scheduled_transactions(request):
    scheduled_transactions = ScheduledTransaction.objects.filter(
        user=request.user, 
        status=ScheduledTransaction.STATUS_PENDING
    ).order_by('due_date')
    
    user_accounts = Account.objects.filter(user=request.user).select_related('subcategory')
    
    return render(request, 'finance/scheduled_transactions.html', {
        'scheduled_transactions': scheduled_transactions,
        'user_accounts': user_accounts,
        'today': timezone.now().date()
    })

@login_required
def liquidate_scheduled_transaction(request, pk):
    scheduled = get_object_or_404(ScheduledTransaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # 1. Criar Lançamento (Transaction)
        Transaction.objects.create(
            user=request.user,
            account=scheduled.account,
            date=scheduled.due_date, # Ou timezone.now().date() se for data do pagamento real
            value=scheduled.value,
            description=f"{scheduled.description} (Liquidado)",
            status=Transaction.STATUS_PENDING # Ou transmitido? Geralmente pendente até transmitir
        )
        
        # 2. Atualizar Status da Agendada
        scheduled.status = ScheduledTransaction.STATUS_PAID
        scheduled.save()
        
        # 3. Lógica de Recorrência
        if scheduled.is_recurring:
            # Ajuste simples para manter o dia (ex: 15/01 -> 15/02)
            import calendar
            year = scheduled.due_date.year + (1 if scheduled.due_date.month == 12 else 0)
            month = 1 if scheduled.due_date.month == 12 else scheduled.due_date.month + 1
            last_day = calendar.monthrange(year, month)[1]
            day = min(scheduled.due_date.day, last_day)
            next_month = scheduled.due_date.replace(year=year, month=month, day=day)
            
            ScheduledTransaction.objects.create(
                user=request.user,
                type=scheduled.type,
                account=scheduled.account,
                description=scheduled.description,
                value=scheduled.value,
                due_date=next_month,
                is_recurring=True,
                status=ScheduledTransaction.STATUS_PENDING
            )
            messages.success(request, 'Conta liquidada e próxima recorrência gerada!')
        else:
            messages.success(request, 'Conta liquidada com sucesso!')
            
    return redirect('finance:list_scheduled_transactions')

@login_required
def delete_scheduled_transaction(request, pk):
    scheduled = get_object_or_404(ScheduledTransaction, pk=pk, user=request.user)
    if request.method == 'POST':
        scheduled.delete()
        messages.success(request, 'Conta agendada excluída com sucesso!')
    return redirect('finance:list_scheduled_transactions')



