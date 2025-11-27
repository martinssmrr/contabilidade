from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    """
    Modelo de usuário customizado para gerenciar diferentes níveis de acesso.
    
    Roles disponíveis:
    - cliente: Usuário final que contrata serviços
    - contador: Profissional de contabilidade que atende clientes
    - admin: Administrador do sistema com acesso total
    - suporte: Equipe de suporte técnico
    """
    
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('contador', 'Contador'),
        ('admin', 'Administrador'),
        ('suporte', 'Suporte'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='cliente',
        verbose_name='Função'
    )
    
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    cpf_cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name='CPF/CNPJ')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"


class MovimentacaoFinanceira(models.Model):
    """Modelo para receitas e despesas do cliente.

    - Vinculado ao usuário (cliente)
    - Pode conter um anexo opcional
    - Status controla ciclo: rascunho -> transmitido -> processado / com pendência
    """

    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    STATUS_RASCUNHO = 'rascunho'
    STATUS_TRANSMITIDO = 'transmitido'
    STATUS_PROCESSADO = 'processado'
    STATUS_COM_PENDENCIA = 'com_pendencia'

    STATUS_CHOICES = [
        (STATUS_RASCUNHO, 'Rascunho'),
        (STATUS_TRANSMITIDO, 'Transmitido'),
        (STATUS_PROCESSADO, 'Processado'),
        (STATUS_COM_PENDENCIA, 'Com Pendência'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    nome = models.CharField(max_length=255)
    competencia = models.DateField(help_text='Use o primeiro dia do mês para representar competência (YYYY-MM-01)')
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    anexo = models.FileField(upload_to='movimentacoes/%Y/%m', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_RASCUNHO)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Movimentação Financeira'
        verbose_name_plural = 'Movimentações Financeiras'
        ordering = ['-competencia', '-created_at']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nome} - {self.valor} ({self.get_status_display()})"

    def is_rascunho(self):
        return self.status == self.STATUS_RASCUNHO

    transmissao = models.ForeignKey(
        'TransmissaoMensal', on_delete=models.SET_NULL, null=True, blank=True, related_name='movimentacoes')


class TransmissaoMensal(models.Model):
    """Representa uma transmissão agrupada de movimentações para um mês/ano."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transmissoes')
    competencia = models.DateField(help_text='Use o primeiro dia do mês para representar competência (YYYY-MM-01)')
    transmitted_at = models.DateTimeField(default=timezone.now)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Transmissão Mensal'
        verbose_name_plural = 'Transmissões Mensais'
        ordering = ['-competencia']

    def __str__(self):
        return f"Transmissão {self.competencia.strftime('%Y-%m')} por {self.user.username} - {self.transmitted_at.date()}"


class CertidaoNegativa(models.Model):
    """Modelo que representa uma Certidão Negativa enviada pelo staff para o cliente."""

    TIPO_FEDERAL = 'federal'
    TIPO_ESTADUAL = 'estadual'
    TIPO_TRABALHISTA = 'trabalhista'
    TIPO_FGTS = 'fgts'

    TIPO_CHOICES = [
        (TIPO_FEDERAL, 'Federal'),
        (TIPO_ESTADUAL, 'Estadual'),
        (TIPO_TRABALHISTA, 'Trabalhista'),
        (TIPO_FGTS, 'FGTS'),
    ]

    STATUS_NEGATIVA = 'negativa'
    STATUS_POSITIVA = 'positiva'
    STATUS_INDISPONIVEL = 'indisponivel'

    STATUS_CHOICES = [
        (STATUS_NEGATIVA, 'Negativa'),
        (STATUS_POSITIVA, 'Positiva'),
        (STATUS_INDISPONIVEL, 'Indisponível'),
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certidoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEGATIVA)
    arquivo_pdf = models.FileField(upload_to='certidoes/%Y/%m')
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Certidão Negativa'
        verbose_name_plural = 'Certidões Negativas'
        ordering = ['-data_envio']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.cliente.username} - {self.get_status_display()} ({self.data_envio.date()})"

