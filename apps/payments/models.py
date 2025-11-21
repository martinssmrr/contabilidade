from django.db import models
from django.conf import settings
from apps.services.models import Service, Plan

# Create your models here.

class Payment(models.Model):
    """
    Modelo para gerenciar pagamentos via Mercado Pago.
    Registra tanto pagamentos de serviços avulsos quanto de assinaturas.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('cancelado', 'Cancelado'),
        ('reembolsado', 'Reembolsado'),
    ]
    
    TIPO_CHOICES = [
        ('servico', 'Serviço Avulso'),
        ('assinatura', 'Assinatura'),
    ]
    
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pagamentos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    
    # Relacionamentos opcionais (um ou outro será preenchido)
    servico = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagamentos')
    plano = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagamentos')
    
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    
    # Informações do Mercado Pago
    mp_payment_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='ID do Pagamento MP')
    mp_preference_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='ID da Preferência MP')
    mp_status = models.CharField(max_length=50, null=True, blank=True, verbose_name='Status MP')
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Pagamento #{self.id} - {self.cliente.username} - R$ {self.valor} ({self.status})"
