from django.db import models
from django.conf import settings
from apps.services.models import Plano
import uuid

class Pagamento(models.Model):
    """
    Modelo para gerenciar pagamentos via Mercado Pago.
    Registra pagamentos de planos de serviço contábil.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processando', 'Processando'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('cancelado', 'Cancelado'),
        ('reembolsado', 'Reembolsado'),
        ('erro', 'Erro'),
    ]
    
    # Identificador único para referência externa
    external_reference = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        help_text="Referência externa única para o Mercado Pago"
    )
    
    # Relacionamento com o plano
    plano = models.ForeignKey(
        Plano, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='pagamentos'
    )
    
    # Cliente (opcional - pode ser anônimo inicialmente)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='pagamentos'
    )
    
    # Dados do cliente (para pagamentos sem login)
    cliente_nome = models.CharField(max_length=200, blank=True, verbose_name='Nome do Cliente')
    cliente_email = models.EmailField(blank=True, verbose_name='E-mail do Cliente')
    cliente_cpf = models.CharField(max_length=14, blank=True, verbose_name='CPF do Cliente')
    cliente_telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone do Cliente')
    
    # Valores
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    
    # Informações do Mercado Pago
    mp_payment_id = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        db_index=True,
        verbose_name='ID do Pagamento MP'
    )
    mp_preference_id = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name='ID da Preferência MP'
    )
    mp_status = models.CharField(max_length=50, null=True, blank=True, verbose_name='Status MP')
    mp_status_detail = models.CharField(max_length=100, null=True, blank=True, verbose_name='Detalhe do Status MP')
    mp_payment_method_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='Método de Pagamento')
    mp_payment_type_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='Tipo de Pagamento')
    
    # Dados adicionais da transação (JSON)
    mp_response_data = models.JSONField(
        null=True, 
        blank=True, 
        verbose_name='Dados da Resposta MP',
        help_text="Dados completos retornados pelo Mercado Pago"
    )
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    pago_em = models.DateTimeField(null=True, blank=True, verbose_name='Pago em')
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['status', 'criado_em']),
            models.Index(fields=['external_reference']),
        ]
    
    def __str__(self):
        cliente_info = self.cliente_email or self.cliente_nome or 'Anônimo'
        plano_nome = self.plano.nome if self.plano else 'Sem plano'
        return f"Pagamento #{self.id} - {plano_nome} - {cliente_info} - R$ {self.valor} ({self.status})"
    
    def is_approved(self):
        """Verifica se o pagamento foi aprovado"""
        return self.status == 'aprovado' or self.mp_status == 'approved'
    
    def get_status_display_class(self):
        """Retorna a classe CSS para o status"""
        status_classes = {
            'pendente': 'warning',
            'processando': 'info',
            'aprovado': 'success',
            'rejeitado': 'danger',
            'cancelado': 'secondary',
            'reembolsado': 'dark',
            'erro': 'danger',
        }
        return status_classes.get(self.status, 'secondary')

