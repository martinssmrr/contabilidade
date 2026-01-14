from django.db import models
from django.conf import settings

def guia_imposto_upload_path(instance, filename):
    return f'guias_impostos/{instance.vencimento.year}/{instance.vencimento.month:02d}/cliente_{instance.cliente.id}/{filename}'

class GuiaImposto(models.Model):
    TIPO_CHOICES = [
        ('das', 'DAS'),
        ('inss', 'INSS'),
        ('fgts', 'FGTS'),
        ('irrf', 'IRRF'),
        ('iss', 'ISS'),
        ('icms', 'ICMS'),
        ('pis', 'PIS'),
        ('cofins', 'COFINS'),
        ('csll', 'CSLL'),
        ('irpj', 'IRPJ'),
        ('outros', 'Outros'),
    ]

    STATUS_CHOICES = [
        ('a_vencer', 'A Vencer'),
        ('pago', 'Pago'),
        ('atrasado', 'Em Atraso'),
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guias_imposto', verbose_name='Cliente')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de Imposto')
    descricao = models.CharField(max_length=200, verbose_name='Descrição', blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    vencimento = models.DateField(verbose_name='Data de Vencimento')
    competencia = models.DateField(verbose_name='Competência (Mês Referência)', help_text="Primeiro dia do mês de referência")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='a_vencer', verbose_name='Status de Pagamento')
    arquivo_pdf = models.FileField(upload_to=guia_imposto_upload_path, verbose_name='Arquivo PDF (Guia)')
    comprovante = models.FileField(upload_to=guia_imposto_upload_path, verbose_name='Comprovante de Pagamento', blank=True, null=True)
    codigo_barras = models.CharField(max_length=100, blank=True, null=True, verbose_name='Código de Barras')
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Guia de Imposto'
        verbose_name_plural = 'Guias de Impostos'
        ordering = ['status', 'vencimento']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.vencimento.strftime('%d/%m/%Y')} - R$ {self.valor}"

    @property
    def is_vencido(self):
        from django.utils import timezone
        return self.status == 'a_vencer' and self.vencimento < timezone.now().date()
