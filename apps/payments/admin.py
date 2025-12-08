from django.contrib import admin
from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'plano', 
        'cliente_email', 
        'valor', 
        'status', 
        'mp_status',
        'mp_payment_id', 
        'criado_em'
    ]
    list_filter = ['status', 'mp_status', 'plano', 'criado_em']
    search_fields = [
        'cliente_nome', 
        'cliente_email', 
        'cliente_cpf',
        'mp_payment_id', 
        'external_reference'
    ]
    readonly_fields = [
        'external_reference',
        'mp_payment_id', 
        'mp_preference_id', 
        'mp_status',
        'mp_status_detail',
        'mp_payment_method_id',
        'mp_payment_type_id',
        'mp_response_data',
        'criado_em', 
        'atualizado_em',
        'pago_em',
    ]
    raw_id_fields = ['cliente', 'plano']
    date_hierarchy = 'criado_em'
    ordering = ['-criado_em']
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('external_reference', 'plano', 'valor', 'status')
        }),
        ('Cliente', {
            'fields': ('cliente', 'cliente_nome', 'cliente_email', 'cliente_cpf', 'cliente_telefone')
        }),
        ('Mercado Pago', {
            'fields': (
                'mp_payment_id', 
                'mp_preference_id', 
                'mp_status', 
                'mp_status_detail',
                'mp_payment_method_id',
                'mp_payment_type_id',
            ),
            'classes': ('collapse',),
        }),
        ('Dados Completos MP (JSON)', {
            'fields': ('mp_response_data',),
            'classes': ('collapse',),
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em', 'pago_em')
        }),
    )
