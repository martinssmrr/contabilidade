from django.contrib import admin
from .models import Lead, Ticket, TicketMessage, Duvida

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
