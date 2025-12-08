from django.db import models
from django.conf import settings

# Create your models here.

class Lead(models.Model):
    """
    Modelo para captação de leads do site.
    Armazena informações de potenciais clientes que preenchem formulários.
    """
    ORIGEM_CHOICES = [
        ('popup', 'Popup da Home'),
        ('contato', 'Seção de Contato'),
    ]
    
    nome_completo = models.CharField(max_length=200, verbose_name='Nome Completo')
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    estado = models.CharField(max_length=2, verbose_name='Estado')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    servico_interesse = models.CharField(max_length=100, verbose_name='Serviço de Interesse')
    origem = models.CharField(max_length=20, choices=ORIGEM_CHOICES, verbose_name='Origem')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro', db_index=True)
    contatado = models.BooleanField(default=False, verbose_name='Foi Contatado?', db_index=True)
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    
    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.nome_completo} - {self.email}"


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


class Cliente(models.Model):
    """
    Perfil do cliente vinculado ao User padrão do Django.
    Cada cliente pode ter um contador_responsavel (staff) associado.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cliente_profile'
    )
    contador_responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes_atendidos'
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Chamado(models.Model):
    """Modelo de Chamado (ticket) para clientes."""
    TIPO_CHOICES = [
        ('nota_fiscal', 'Emissão de Notas Fiscais'),
        ('documentos', 'Documentos da Empresa'),
        ('boleto', 'Boleto Bancário'),
        ('outros', 'Outros'),
    ]

    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('resolvido', 'Resolvido'),
        ('fechado', 'Fechado'),
    ]

    cliente = models.ForeignKey(
        'support.Cliente',
        on_delete=models.CASCADE,
        related_name='chamados'
    )
    titulo = models.CharField(max_length=200)
    tipo_solicitacao = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='media')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chamado'
        verbose_name_plural = 'Chamados'
        ordering = ['-data_criacao']

    def __str__(self):
        return f"#{self.pk} - {self.titulo} ({self.get_status_display()})"


class ChamadoAttachment(models.Model):
    """Arquivos anexados diretamente a um Chamado (enviados na criação)."""
    chamado = models.ForeignKey(
        'support.Chamado', on_delete=models.CASCADE, related_name='anexos'
    )
    arquivo = models.FileField(upload_to='chamados/anexos/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Anexo de Chamado'
        verbose_name_plural = 'Anexos de Chamados'

    def __str__(self):
        return f"Anexo #{self.pk} para Chamado #{self.chamado.pk}"


class ChamadoMessage(models.Model):
    """Mensagens/Respostas dentro de um Chamado.

    Permite que tanto o cliente quanto o staff/admin respondam com texto e um anexo opcional.
    """
    chamado = models.ForeignKey(
        Chamado, on_delete=models.CASCADE, related_name='mensagens'
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    mensagem = models.TextField()
    anexo = models.FileField(upload_to='chamados/mensagens/%Y/%m/%d/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagem de Chamado'
        verbose_name_plural = 'Mensagens de Chamados'
        ordering = ['criado_em']

    def __str__(self):
        autor = self.autor.get_full_name() if self.autor else 'Sistema'
        return f"Mensagem de {autor} em Chamado #{self.chamado.pk}"
