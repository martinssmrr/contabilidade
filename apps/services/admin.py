from django.contrib import admin
from .models import Service, Plan, Subscription, ProcessoAbertura, Socio, Plano, CategoriaCNAE, CNAE

# Register your models here.


@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'preco_antigo', 'ativo', 'destaque', 'ordem']
    list_filter = ['categoria', 'ativo', 'destaque']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo', 'destaque', 'ordem']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'categoria', 'descricao', 'ordem')
        }),
        ('Preços', {
            'fields': ('preco', 'preco_antigo')
        }),
        ('Características', {
            'fields': ('features',),
            'description': 'Adicione as características do plano em formato de lista JSON. Exemplo: ["Contabilidade completa", "Certificado digital incluído"]'
        }),
        ('Integração Mercado Pago', {
            'fields': ('mercadopago_price_id',),
            'classes': ('collapse',)
        }),
        ('Configurações', {
            'fields': ('ativo', 'destaque')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('categoria', 'ordem', 'preco')


class SocioInline(admin.TabularInline):
    model = Socio
    extra = 0
    fields = ['nome_completo', 'cpf', 'percentual_participacao']


@admin.register(ProcessoAbertura)
class ProcessoAberturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_completo', 'tipo_societario', 'status', 'etapa_atual', 'criado_em']
    list_filter = ['status', 'tipo_societario', 'etapa_atual', 'criado_em']
    search_fields = ['nome_completo', 'cpf', 'email']
    readonly_fields = ['criado_em', 'atualizado_em', 'data_assinatura', 'data_pagamento']
    inlines = [SocioInline]
    
    fieldsets = (
        ('Informações do Processo', {
            'fields': ('usuario', 'status', 'etapa_atual', 'criado_em', 'atualizado_em')
        }),
        ('Dados Pessoais', {
            'fields': ('nome_completo', 'data_nascimento', 'cpf', 'rg', 'orgao_emissor', 
                      'uf_emissao', 'telefone_whatsapp', 'email', 'estado_civil', 'nome_mae', 'profissao'),
            'classes': ('collapse',)
        }),
        ('Endereço Residencial', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado'),
            'classes': ('collapse',)
        }),
        ('Dados da Empresa', {
            'fields': ('tipo_societario', 'nome_fantasia_mei', 'nome_fantasia_me', 'razao_social', 
                      'capital_social', 'quantidade_socios', 'regime_tributario'),
            'classes': ('collapse',)
        }),
        ('Pagamento', {
            'fields': ('plano_selecionado', 'cupom_desconto', 'valor_pago', 'data_pagamento', 'pagamento_confirmado'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf', 'percentual_participacao', 'processo']
    search_fields = ['nome_completo', 'cpf']
    list_filter = ['estado_civil']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'periodo', 'ativo', 'criado_em']
    list_filter = ['periodo', 'ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'plano', 'status', 'data_inicio', 'data_fim']
    list_filter = ['status', 'data_inicio']
    search_fields = ['cliente__username', 'cliente__email', 'plano__nome']
    raw_id_fields = ['cliente', 'plano']


@admin.register(CategoriaCNAE)
class CategoriaCNAEAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ordem', 'total_cnaes', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['nome']
    list_editable = ['ordem']
    ordering = ['ordem', 'nome']


@admin.register(CNAE)
class CNAEAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao_curta', 'categoria', 'ativo', 'criado_em']
    list_filter = ['categoria', 'ativo', 'criado_em']
    search_fields = ['codigo', 'descricao', 'categoria__nome']
    list_editable = ['ativo']
    ordering = ['categoria__ordem', 'categoria__nome', 'codigo']
    
    def descricao_curta(self, obj):
        """Retorna descrição limitada a 60 caracteres"""
        return obj.descricao[:60] + '...' if len(obj.descricao) > 60 else obj.descricao
    descricao_curta.short_description = 'Descrição'
