from django.db import models
from django.conf import settings
from django.utils import timezone

class Subcategory(models.Model):
    TYPE_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='finance_subcategories')
    name = models.CharField(max_length=100, verbose_name='Nome da Subcategoria')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Tipo')
    
    class Meta:
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'
        ordering = ['type', 'name']
        unique_together = ['user', 'name', 'type']

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='finance_accounts')
    # subcategory será deprecado em favor da estrutura hierarquica, mantendo por enquanto para migração
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='accounts', verbose_name='Subcategoria', null=True, blank=True)
    
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Conta Pai')
    code = models.CharField(max_length=20, verbose_name='Código Contábil', blank=True, null=True, help_text='Ex: 1.1.01')
    name = models.CharField(max_length=100, verbose_name='Nome da Conta')
    is_synthetic = models.BooleanField(default=False, verbose_name='Conta Sintética (Agrupadora)')
    
    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['code', 'name']
        unique_together = [] # Removido unique anterior pois mudou a logica

    def __str__(self):
        prefix = f"{self.code} - " if self.code else ""
        return f"{prefix}{self.name}"

    def get_level(self):
        """Retorna o nível de indentação da conta baseada no código"""
        if not self.code: return 0
        return self.code.count('.')


class Transaction(models.Model):
    STATUS_PENDING = 'pendente'
    STATUS_TRANSMITTED = 'transmitido'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendente'),
        (STATUS_TRANSMITTED, 'Transmitido'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='finance_transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', verbose_name='Conta')
    date = models.DateField(default=timezone.now, verbose_name='Data da Transação')
    value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor (R$)')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Descrição')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lançamento'
        verbose_name_plural = 'Lançamentos'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.account.name} - R$ {self.value}"
    
    @property
    def type(self):
        return self.account.subcategory.type

class ScheduledTransaction(models.Model):
    TYPE_CHOICES = [
        ('entrada', 'A Receber'),
        ('saida', 'A Pagar'),
    ]
    
    STATUS_PENDING = 'pendente'
    STATUS_PAID = 'pago'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendente'),
        (STATUS_PAID, 'Liquidado'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='finance_scheduled')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Tipo')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='scheduled_transactions', verbose_name='Conta/Categoria')
    description = models.CharField(max_length=255, verbose_name='Fornecedor/Cliente')
    value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor (R$)')
    due_date = models.DateField(verbose_name='Data de Vencimento')
    is_recurring = models.BooleanField(default=False, verbose_name='Recorrente (Mensal)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Conta Agendada'
        verbose_name_plural = 'Contas Agendadas'
        ordering = ['due_date']

    def __str__(self):
        return f"{self.get_type_display()} - {self.description} - {self.value}"

class BankReconciliation(models.Model):
    STATUS_PENDING = 'pendente'
    STATUS_IMPORTED = 'importado'
    STATUS_IGNORED = 'ignorado'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendente'),
        (STATUS_IMPORTED, 'Aprovado'),
        (STATUS_IGNORED, 'Ignorado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='finance_reconciliations')
    date = models.DateField(verbose_name='Data')
    description = models.CharField(max_length=255, verbose_name='Descrição (OFX)')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor')
    fitid = models.CharField(max_length=255, verbose_name='ID Transação Banco')
    suggested_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Categoria Sugerida')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conciliação'
        verbose_name_plural = 'Conciliações'
        unique_together = ['fitid', 'user'] # Evita duplicidade de importação do mesmo OFX

    def __str__(self):
        return f"{self.description} - {self.amount}"

