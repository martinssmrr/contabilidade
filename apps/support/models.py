from django.db import models
from django.conf import settings

# Create your models here.

class Ticket(models.Model):
    """
    Modelo para sistema de tickets de suporte.
    Permite que clientes abram solicitações e a equipe acompanhe o atendimento.
    """
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('aguardando_cliente', 'Aguardando Cliente'),
        ('concluido', 'Concluído'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tickets_cliente',
        verbose_name='Cliente'
    )
    staff_designado = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='tickets_staff',
        limit_choices_to={'role__in': ['admin', 'suporte', 'contador']},
        verbose_name='Staff Designado'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto', verbose_name='Status')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='media', verbose_name='Prioridade')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Ticket #{self.id} - {self.titulo} ({self.get_status_display()})"


class TicketMessage(models.Model):
    """
    Modelo para mensagens dentro de um ticket (conversação).
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Autor')
    mensagem = models.TextField(verbose_name='Mensagem')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Mensagem do Ticket'
        verbose_name_plural = 'Mensagens dos Tickets'
        ordering = ['criado_em']
    
    def __str__(self):
        return f"Mensagem de {self.autor.username} em Ticket #{self.ticket.id}"


class Duvida(models.Model):
    """
    Modelo para FAQ (Perguntas Frequentes).
    Permite gerenciar dúvidas comuns através do admin do Django.
    """
    titulo = models.CharField(max_length=300, verbose_name='Pergunta')
    descricao = models.TextField(verbose_name='Resposta')
    ordem = models.IntegerField(default=0, verbose_name='Ordem de Exibição', help_text='Ordem de exibição no site (menor número aparece primeiro)')
    ativo = models.BooleanField(default=True, verbose_name='Ativo', help_text='Desmarque para ocultar esta dúvida do site')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Dúvida Frequente'
        verbose_name_plural = 'Dúvidas Frequentes'
        ordering = ['ordem', '-criado_em']
    
    def __str__(self):
        return self.titulo
