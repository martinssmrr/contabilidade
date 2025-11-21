from django.contrib import admin
from .models import Ticket, TicketMessage, Duvida

# Register your models here.

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
