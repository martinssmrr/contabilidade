from django.contrib import admin
from .models import Lead, Ticket, TicketMessage, Duvida, Cliente, Chamado
from .models import ChamadoAttachment, ChamadoMessage
from .models import ChatbotPergunta, ChatbotSessao, ChatbotMensagem

# Register your models here.

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'email', 'telefone', 'servico_interesse', 'origem', 'contatado', 'criado_em']
    list_filter = ['origem', 'contatado', 'estado', 'criado_em']
    search_fields = ['nome_completo', 'email', 'telefone', 'cidade']
    list_editable = ['contatado']
    readonly_fields = ['criado_em']
    fieldsets = (
        ('Informações do Lead', {
            'fields': ('nome_completo', 'email', 'telefone')
        }),
        ('Localização', {
            'fields': ('estado', 'cidade')
        }),
        ('Interesse', {
            'fields': ('servico_interesse', 'origem')
        }),
        ('Acompanhamento', {
            'fields': ('contatado', 'observacoes', 'criado_em')
        }),
    )

class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 0
    readonly_fields = ['autor', 'mensagem', 'criado_em']
    can_delete = False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'cliente', 'staff_designado', 'status', 'prioridade', 'criado_em']
    list_filter = ['status', 'prioridade', 'criado_em']
    search_fields = ['titulo', 'descricao', 'cliente__username']
    raw_id_fields = ['cliente', 'staff_designado']
    inlines = [TicketMessageInline]


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'autor', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['mensagem', 'autor__username']
    raw_id_fields = ['ticket', 'autor']


@admin.register(Duvida)
class DuvidaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ordem', 'ativo', 'criado_em', 'atualizado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['titulo', 'descricao']
    list_editable = ['ordem', 'ativo']
    ordering = ['ordem', '-criado_em']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Admin para perfis de cliente."""
    list_display = ['user', 'cnpj', 'razao_social', 'fase_abertura', 'contador_responsavel']
    list_filter = ['fase_abertura', 'regime_tributario', 'endereco_virtual_status', 'certificado_digital_status']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'cnpj', 'razao_social']
    raw_id_fields = ['user', 'contador_responsavel']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user', 'contador_responsavel')
        }),
        ('Status de Abertura', {
            'fields': ('fase_abertura', 'regime_tributario')
        }),
        ('Dados da Empresa', {
            'fields': ('cnpj', 'razao_social', 'nome_fantasia', 'endereco', 'telefone'),
            'classes': ('wide',)
        }),
        ('Endereço Virtual', {
            'fields': ('endereco_virtual_status', 'endereco_virtual_endereco', 'endereco_virtual_validade'),
            'classes': ('collapse',)
        }),
        ('Certificado Digital', {
            'fields': ('certificado_digital_status', 'certificado_digital_tipo', 'certificado_digital_validade'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    """Admin para Chamado com listagem e filtros solicitados."""
    list_display = ['cliente', 'titulo', 'tipo_solicitacao', 'status', 'data_criacao']
    list_filter = ['status', 'tipo_solicitacao']
    search_fields = ['titulo', 'descricao', 'cliente__user__username', 'cliente__user__first_name', 'cliente__user__last_name']
    raw_id_fields = ['cliente']
    
    class ChamadoAttachmentInline(admin.TabularInline):
        model = ChamadoAttachment
        extra = 0
        readonly_fields = ['uploaded_by', 'criado_em']

    class ChamadoMessageInline(admin.StackedInline):
        model = ChamadoMessage
        extra = 0
        readonly_fields = ['criado_em']

    inlines = [ChamadoAttachmentInline, ChamadoMessageInline]


# ========================================
# CHATBOT - Admin
# ========================================

@admin.register(ChatbotPergunta)
class ChatbotPerguntaAdmin(admin.ModelAdmin):
    list_display = ['pergunta', 'categoria', 'ordem', 'ativo', 'criado_em']
    list_filter = ['ativo', 'categoria', 'criado_em']
    search_fields = ['pergunta', 'resposta', 'palavras_chave']
    list_editable = ['ordem', 'ativo']
    ordering = ['categoria', 'ordem']
    fieldsets = (
        ('Pergunta e Resposta', {
            'fields': ('pergunta', 'resposta')
        }),
        ('Configurações', {
            'fields': ('categoria', 'palavras_chave', 'ordem', 'ativo')
        }),
    )


class ChatbotMensagemInline(admin.TabularInline):
    model = ChatbotMensagem
    extra = 0
    readonly_fields = ['is_bot', 'conteudo', 'pergunta_relacionada', 'criado_em']
    can_delete = False


@admin.register(ChatbotSessao)
class ChatbotSessaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'status', 'avaliacao', 'criado_em']
    list_filter = ['status', 'avaliacao', 'criado_em']
    search_fields = ['nome', 'email', 'telefone']
    readonly_fields = ['session_key', 'lead', 'pagina_origem', 'ip_address', 'criado_em', 'encerrado_em']
    inlines = [ChatbotMensagemInline]
    fieldsets = (
        ('Visitante', {
            'fields': ('nome', 'email', 'telefone', 'lead')
        }),
        ('Status', {
            'fields': ('status', 'avaliacao', 'feedback')
        }),
        ('Metadados', {
            'fields': ('session_key', 'pagina_origem', 'ip_address', 'criado_em', 'encerrado_em'),
            'classes': ('collapse',)
        }),
    )
