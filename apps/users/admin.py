from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import MovimentacaoFinanceira
from .models import TransmissaoMensal
from .models import CertidaoNegativa
from django.utils.html import format_html

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Configuração do admin para o modelo CustomUser.
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'cpf_cnpj']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('role', 'telefone', 'cpf_cnpj')}),
    )


@admin.register(MovimentacaoFinanceira)
class MovimentacaoFinanceiraAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tipo', 'nome', 'competencia', 'valor', 'status', 'created_at')
    list_filter = ('status', 'tipo', 'competencia')
    search_fields = ('nome', 'user__username', 'user__first_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-competencia', '-created_at')

    fieldsets = (
        (None, {'fields': ('user', 'tipo', 'nome', 'competencia', 'valor', 'anexo', 'status')}),
        ('Metadados', {'fields': ('created_at', 'updated_at')}),
    )

    def anexo_preview(self, obj):
        if obj.anexo:
            return format_html('<a href="{}" target="_blank">Ver anexo</a>', obj.anexo.url)
        return '-'

    anexo_preview.short_description = 'Anexo'


class MovimentacaoInline(admin.TabularInline):
    model = MovimentacaoFinanceira
    fields = ('tipo', 'nome', 'competencia', 'valor', 'status', 'anexo_preview')
    # anexo_preview is not a model attribute; show raw anexo field as readonly instead
    fields = ('tipo', 'nome', 'competencia', 'valor', 'status', 'anexo')
    readonly_fields = ('anexo',)
    extra = 0


@admin.register(TransmissaoMensal)
class TransmissaoMensalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'competencia', 'transmitted_at')
    list_filter = ('competencia', 'transmitted_at')
    inlines = (MovimentacaoInline,)


@admin.register(CertidaoNegativa)
class CertidaoNegativaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tipo', 'status', 'data_envio', 'arquivo_preview')
    list_filter = ('tipo', 'status', 'data_envio')
    search_fields = ('cliente__username', 'cliente__first_name', 'cliente__email')
    readonly_fields = ('data_envio',)

    def arquivo_preview(self, obj):
        if obj.arquivo_pdf:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.arquivo_pdf.url)
        return '-'

    arquivo_preview.short_description = 'Arquivo'
