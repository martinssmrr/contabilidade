from django.contrib import admin
from .models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'tipo', 'valor', 'status', 'mp_payment_id', 'criado_em']
    list_filter = ['tipo', 'status', 'criado_em']
    search_fields = ['cliente__username', 'cliente__email', 'mp_payment_id']
    readonly_fields = ['mp_payment_id', 'mp_preference_id', 'mp_status', 'criado_em', 'atualizado_em']
    raw_id_fields = ['cliente', 'servico', 'plano']
