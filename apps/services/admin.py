from django.contrib import admin
from .models import Service, Plan, Subscription, ProcessoAbertura, Socio, Plano, CategoriaCNAE, CNAE, SolicitacaoAberturaMEI, ServicoAvulso, ContratacaoServicoAvulso, SolicitacaoBaixaMEI, SolicitacaoDeclaracaoAnualMEI

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
        ('Recursos Incluídos ✅', {
            'fields': ('features_included',),
            'description': 'Adicione os recursos que ESTÃO incluídos neste plano. Formato: ["Item 1", "Item 2"]. Exemplo: ["Contabilidade Completa", "Certificado Digital", "Suporte WhatsApp"]'
        }),
        ('Recursos NÃO Incluídos ❌', {
            'fields': ('features_excluded',),
            'description': 'Adicione os recursos que NÃO estão incluídos neste plano. Formato: ["Item 1", "Item 2"]. Exemplo: ["Folha de Pagamentos", "Consultoria Tributária"]'
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


# =============================================================================
# ADMIN PARA SOLICITAÇÕES DE ABERTURA MEI
# =============================================================================

@admin.register(SolicitacaoAberturaMEI)
class SolicitacaoAberturaMEIAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar solicitações de abertura de MEI.
    Permite visualizar, filtrar e editar solicitações de clientes.
    """
    
    list_display = [
        'id', 
        'nome_completo', 
        'cpf_formatado', 
        'email', 
        'cnae_primario', 
        'status', 
        'criado_em'
    ]
    
    list_filter = [
        'status', 
        'estado', 
        'forma_atuacao', 
        'criado_em'
    ]
    
    search_fields = [
        'nome_completo', 
        'cpf', 
        'email', 
        'telefone', 
        'cnae_primario'
    ]
    
    readonly_fields = [
        'criado_em', 
        'atualizado_em', 
        'cpf_formatado', 
        'telefone_formatado',
        'endereco_completo'
    ]
    
    list_editable = ['status']
    
    date_hierarchy = 'criado_em'
    
    ordering = ['-criado_em']
    
    fieldsets = (
        ('Informações do Processo', {
            'fields': ('status', 'criado_em', 'atualizado_em', 'pagamento')
        }),
        ('Dados Pessoais', {
            'fields': (
                'nome_completo', 
                'email', 
                'telefone', 
                'cpf',
                'rg', 
                'orgao_expedidor_rg', 
                'uf_orgao_expedidor'
            )
        }),
        ('Atividade do MEI', {
            'fields': (
                'cnae_primario', 
                'cnae_secundario', 
                'forma_atuacao', 
                'capital_social'
            )
        }),
        ('Endereço', {
            'fields': (
                'cep', 
                'logradouro', 
                'numero', 
                'complemento', 
                'bairro', 
                'cidade', 
                'estado'
            ),
            'classes': ('collapse',)
        }),
        ('Observações Internas', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marcar_como_pago', 'marcar_em_andamento', 'marcar_concluido']
    
    def marcar_como_pago(self, request, queryset):
        """Ação para marcar solicitações como pagas"""
        updated = queryset.update(status='pago')
        self.message_user(request, f'{updated} solicitação(ões) marcada(s) como paga(s).')
    marcar_como_pago.short_description = 'Marcar como Pago'
    
    def marcar_em_andamento(self, request, queryset):
        """Ação para marcar solicitações como em andamento"""
        updated = queryset.update(status='em_andamento')
        self.message_user(request, f'{updated} solicitação(ões) marcada(s) como em andamento.')
    marcar_em_andamento.short_description = 'Marcar como Em Andamento'
    
    def marcar_concluido(self, request, queryset):
        """Ação para marcar solicitações como concluídas"""
        updated = queryset.update(status='concluido')
        self.message_user(request, f'{updated} solicitação(ões) marcada(s) como concluída(s).')
    marcar_concluido.short_description = 'Marcar como Concluído'


# =============================================================================
# ADMIN PARA SERVIÇOS AVULSOS
# =============================================================================

@admin.register(ServicoAvulso)
class ServicoAvulsoAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar serviços avulsos disponíveis para contratação.
    """
    list_display = ['titulo', 'valor', 'icone', 'ativo', 'ordem', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['titulo', 'descricao']
    list_editable = ['ativo', 'ordem', 'valor']
    ordering = ['ordem', 'titulo']
    
    fieldsets = (
        ('Informações do Serviço', {
            'fields': ('titulo', 'descricao', 'valor')
        }),
        ('Configurações de Exibição', {
            'fields': ('icone', 'ordem', 'ativo')
        }),
    )


@admin.register(ContratacaoServicoAvulso)
class ContratacaoServicoAvulsoAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar contratações de serviços avulsos.
    """
    list_display = [
        'id',
        'usuario',
        'servico',
        'status',
        'valor_contratado',
        'visualizado',
        'criado_em'
    ]
    list_filter = ['status', 'visualizado', 'servico', 'criado_em']
    search_fields = ['usuario__email', 'usuario__first_name', 'servico__titulo']
    list_editable = ['status', 'visualizado']
    readonly_fields = ['criado_em', 'atualizado_em', 'concluido_em']
    date_hierarchy = 'criado_em'
    ordering = ['-criado_em']
    raw_id_fields = ['usuario']
    
    fieldsets = (
        ('Informações da Contratação', {
            'fields': ('usuario', 'servico', 'status', 'valor_contratado')
        }),
        ('Observações', {
            'fields': ('observacoes_cliente', 'observacoes_internas'),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': ('visualizado', 'criado_em', 'atualizado_em', 'concluido_em')
        }),
    )
    
    actions = ['marcar_em_andamento', 'marcar_concluido', 'marcar_visualizado']
    
    def marcar_em_andamento(self, request, queryset):
        updated = queryset.update(status='em_andamento', visualizado=True)
        self.message_user(request, f'{updated} contratação(ões) marcada(s) como em andamento.')
    marcar_em_andamento.short_description = 'Marcar como Em Andamento'
    
    def marcar_concluido(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='concluido', concluido_em=timezone.now())
        self.message_user(request, f'{updated} contratação(ões) marcada(s) como concluída(s).')
    marcar_concluido.short_description = 'Marcar como Concluído'
    
    def marcar_visualizado(self, request, queryset):
        updated = queryset.update(visualizado=True)
        self.message_user(request, f'{updated} contratação(ões) marcada(s) como visualizada(s).')
    marcar_visualizado.short_description = 'Marcar como Visualizado'


@admin.register(SolicitacaoBaixaMEI)
class SolicitacaoBaixaMEIAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'email', 'cnpj', 'cpf', 'motivo', 'status', 'pagamento', 'criado_em']
    list_filter = ['status', 'motivo', 'criado_em']
    search_fields = ['nome_completo', 'email', 'cnpj', 'cpf']
    list_editable = ['status']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['-criado_em']


@admin.register(SolicitacaoDeclaracaoAnualMEI)
class SolicitacaoDeclaracaoAnualMEIAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'email', 'cnpj', 'ano_referencia', 'faturamento', 'teve_funcionario', 'status', 'pagamento', 'criado_em']
    list_filter = ['status', 'ano_referencia', 'teve_funcionario', 'criado_em']
    search_fields = ['nome_completo', 'email', 'cnpj']
    list_editable = ['status']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['-criado_em']
