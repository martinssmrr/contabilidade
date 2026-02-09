from django.db import models
from django.conf import settings
from django.utils import timezone
from typing import Optional
import os
from .models_guia_imposto import GuiaImposto

# Create your models here.

def document_upload_path(instance, filename):
    """
    Define o caminho de upload dos documentos.
    Organiza por tipo de usuário e ID do usuário.
    """
    user_role = instance.usuario.role
    user_id = instance.usuario.id
    return f'documents/{user_role}/{user_id}/{filename}'


class Document(models.Model):
    """
    Modelo para gerenciamento de documentos e arquivos.
    Usado para uploads de relatórios (PDFs), contratos, comprovantes, etc.
    """
    CATEGORIA_CHOICES = [
        ('relatorio', 'Relatório'),
        ('contrato', 'Contrato'),
        ('comprovante', 'Comprovante'),
        ('declaracao', 'Declaração'),
        ('nota_fiscal', 'Nota Fiscal'),
        ('outros', 'Outros'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    arquivo = models.FileField(upload_to=document_upload_path, verbose_name='Arquivo')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='outros', verbose_name='Categoria')
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='documentos',
        verbose_name='Usuário'
    )
    
    # Controle de visibilidade
    visivel_para_cliente = models.BooleanField(default=True, verbose_name='Visível para Cliente')
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    @property
    def tamanho_arquivo(self):
        """Retorna o tamanho do arquivo em formato legível."""
        if self.arquivo:
            size = self.arquivo.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 B"
    
    @property
    def extensao_arquivo(self):
        """Retorna a extensão do arquivo."""
        if self.arquivo:
            return os.path.splitext(self.arquivo.name)[1].lower()
        return None


def nota_fiscal_upload_path(instance, filename):
    """
    Define o caminho de upload das notas fiscais.
    Organiza por ano/mês e ID do cliente.
    """
    from datetime import datetime
    now = datetime.now()
    return f'notas_fiscais/{now.year}/{now.month:02d}/cliente_{instance.cliente.id}/{filename}'


class NotaFiscal(models.Model):
    """
    Modelo para gerenciamento de Notas Fiscais enviadas pela equipe aos clientes.
    """
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notas_fiscais',
        verbose_name='Cliente',
        help_text='Cliente que receberá a nota fiscal'
    )
    
    arquivo_pdf = models.FileField(
        upload_to=nota_fiscal_upload_path,
        verbose_name='Arquivo PDF',
        help_text='Envie o arquivo da nota fiscal em formato PDF'
    )
    
    data_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data do Upload'
    )
    
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='notas_fiscais_enviadas',
        limit_choices_to={'is_staff': True},
        verbose_name='Enviado por',
        help_text='Membro da equipe que fez o upload'
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações',
        help_text='Observações internas sobre esta nota fiscal'
    )
    
    class Meta:
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
        ordering = ['-data_upload']
    
    def __str__(self):
        return f"NF - {self.cliente.get_full_name() or self.cliente.username} - {self.data_upload.strftime('%d/%m/%Y')}"
    
    @property
    def nome_arquivo(self):
        """Retorna apenas o nome do arquivo sem o caminho."""
        if self.arquivo_pdf:
            return os.path.basename(self.arquivo_pdf.name)
        return "Sem arquivo"
    
    @property
    def tamanho_arquivo(self):
        """Retorna o tamanho do arquivo em formato legível."""
        if self.arquivo_pdf:
            size = self.arquivo_pdf.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 B"


def documento_empresa_upload_path(instance, filename):
    """
    Define o caminho de upload dos documentos da empresa.
    Organiza por ano/mês e ID do cliente.
    """
    from datetime import datetime
    now = datetime.now()
    return f'documentos_empresa/{now.year}/{now.month:02d}/cliente_{instance.cliente.id}/{filename}'


class DocumentoEmpresa(models.Model):
    """
    Modelo para gerenciamento de Documentos da Empresa enviados pela equipe aos clientes.
    Exibe nome do documento + arquivo para download.
    """
    CATEGORIA_CHOICES = [
        ('contrato_social', 'Contrato Social'),
        ('alvara', 'Alvará'),
        ('certidao', 'Certidão'),
        ('procuracao', 'Procuração'),
        ('registro', 'Registro'),
        ('declaracao', 'Declaração'),
        ('relatorio', 'Relatório'),
        ('outros', 'Outros'),
    ]
    
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documentos_empresa',
        verbose_name='Cliente',
        help_text='Cliente que receberá o documento'
    )
    
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título do Documento',
        help_text='Nome descritivo do documento (ex: Contrato Social da Empresa, Alvará de Funcionamento)'
    )
    
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='outros',
        verbose_name='Categoria',
        help_text='Tipo do documento'
    )
    
    arquivo = models.FileField(
        upload_to=documento_empresa_upload_path,
        verbose_name='Arquivo',
        help_text='Envie o arquivo do documento (PDF, DOC, DOCX, etc.)'
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição',
        help_text='Descrição adicional sobre o documento (opcional)'
    )
    
    data_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data do Upload'
    )
    
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documentos_empresa_enviados',
        limit_choices_to={'is_staff': True},
        verbose_name='Enviado por',
        help_text='Membro da equipe que fez o upload'
    )
    
    class Meta:
        verbose_name = 'Documento da Empresa'
        verbose_name_plural = 'Documentos da Empresa'
        ordering = ['-data_upload']
    
    def __str__(self):
        return f"{self.titulo} - {self.cliente.get_full_name() or self.cliente.username}"
    
    @property
    def nome_arquivo(self):
        """Retorna apenas o nome do arquivo sem o caminho."""
        if self.arquivo:
            return os.path.basename(self.arquivo.name)
        return "Sem arquivo"
    
    @property
    def tamanho_arquivo(self):
        """Retorna o tamanho do arquivo em formato legível."""
        if self.arquivo:
            size = self.arquivo.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 B"
    
    @property
    def extensao_arquivo(self):
        """Retorna a extensão do arquivo."""
        if self.arquivo:
            return os.path.splitext(self.arquivo.name)[1].lower().replace('.', '')
        return None


def extrato_bancario_upload_path(instance, filename):
    """
    Define o caminho de upload dos extratos bancários.
    Organiza por cliente e mês/ano.
    """
    # Preferir usar período (start/end) quando disponível
    if getattr(instance, 'start_date', None) and getattr(instance, 'end_date', None):
        s = instance.start_date.strftime('%Y%m%d')
        e = instance.end_date.strftime('%Y%m%d')
        folder = f'{s}_{e}'
    else:
        mes_ano = (getattr(instance, 'mes_ano', '') or '').replace('/', '_')
        folder = mes_ano or 'sem_periodo'

    return f'extratos_bancarios/cliente_{instance.cliente.id}/{folder}/{filename}'


class ExtratoBancario(models.Model):
    """
    Modelo para gerenciamento de Extratos Bancários enviados pelos clientes.
    O cliente faz upload dos seus próprios extratos.
    """
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='extratos_bancarios',
        verbose_name='Cliente',
        help_text='Cliente que enviou o extrato'
    )
    
    mes_ano = models.CharField(
        max_length=7,
        verbose_name='Mês/Ano',
        help_text='Mês e ano do extrato (ex: 01/2025, 11/2024)'
    )
    # Período opcional: data inicial e final
    start_date = models.DateField(blank=True, null=True, verbose_name='Data inicial do período')
    end_date = models.DateField(blank=True, null=True, verbose_name='Data final do período')
    
    arquivo = models.FileField(
        upload_to=extrato_bancario_upload_path,
        verbose_name='Arquivo do Extrato',
        help_text='Envie o arquivo do extrato bancário (PDF, imagem, etc.)'
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações',
        help_text='Observações adicionais sobre este extrato (opcional)'
    )
    
    data_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data do Upload'
    )
    
    class Meta:
        verbose_name = 'Extrato Bancário'
        verbose_name_plural = 'Extratos Bancários'
        ordering = ['-data_upload']
        unique_together = [['cliente', 'mes_ano', 'arquivo']]
    
    def __str__(self):
        return f"Extrato {self.mes_ano} - {self.cliente.get_full_name() or self.cliente.username}"
    
    @property
    def nome_arquivo(self):
        """Retorna apenas o nome do arquivo sem o caminho."""
        if self.arquivo:
            return os.path.basename(self.arquivo.name)
        return "Sem arquivo"
    
    @property
    def tamanho_arquivo(self):
        """Retorna o tamanho do arquivo em formato legível."""
        if self.arquivo:
            size = self.arquivo.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 B"
    
    @property
    def extensao_arquivo(self):
        """Retorna a extensão do arquivo."""
        if self.arquivo:
            return os.path.splitext(self.arquivo.name)[1].lower().replace('.', '')
        return None


def documento_cliente_upload_path(instance, filename):
    """
    Define o caminho de upload dos documentos de clientes.
    Organiza por ano/mês do envio e ID do cliente.
    """
    now = timezone.now()
    return f'documentos_clientes/{now.year}/{now.month:02d}/cliente_{instance.cliente.id}/{filename}'


class DocumentoCliente(models.Model):
    """
    Modelo para gerenciamento de documentos enviados pelo staff aos clientes.
    Com notificação automática por e-mail (sem anexar o documento - LGPD).
    """
    
    TIPO_DOCUMENTO_CHOICES = [
        ('contrato_social', 'Contrato Social'),
        ('alteracao_contratual', 'Alteração Contratual'),
        ('certidao_negativa', 'Certidão Negativa'),
        ('guia_impostos', 'Guia de Impostos'),
        ('balanco_patrimonial', 'Balanço Patrimonial'),
        ('dre', 'DRE - Demonstração do Resultado'),
        ('folha_pagamento', 'Folha de Pagamento'),
        ('declaracao_ir', 'Declaração de IR'),
        ('alvara', 'Alvará'),
        ('licenca', 'Licença'),
        ('procuracao', 'Procuração'),
        ('relatorio_contabil', 'Relatório Contábil'),
        ('documento_fiscal', 'Documento Fiscal'),
        ('outros', 'Outros'),
    ]
    
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documentos_recebidos',
        verbose_name='Cliente',
        help_text='Cliente que receberá este documento',
        limit_choices_to={'is_staff': False},
    )
    
    arquivo = models.FileField(
        upload_to=documento_cliente_upload_path,
        verbose_name='Arquivo',
        help_text='Arquivo do documento (PDF, DOC, DOCX, XLS, etc.)',
        max_length=500,
    )
    
    tipo_documento = models.CharField(
        max_length=30,
        choices=TIPO_DOCUMENTO_CHOICES,
        verbose_name='Tipo de Documento',
        help_text='Categoria/tipo do documento',
        db_index=True,
    )
    
    titulo = models.CharField(
        max_length=255,
        verbose_name='Título',
        help_text='Título descritivo do documento',
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição',
        help_text='Descrição adicional ou observações sobre o documento (opcional)',
    )
    
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documentos_enviados_clientes',
        limit_choices_to={'is_staff': True},
        verbose_name='Enviado por',
        help_text='Membro da equipe que fez o upload',
    )
    
    data_envio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Envio',
        db_index=True,
    )
    
    visualizado = models.BooleanField(
        default=False,
        verbose_name='Visualizado',
        help_text='Indica se o cliente já visualizou este documento',
    )
    
    data_visualizacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Visualização',
    )
    
    notificacao_enviada = models.BooleanField(
        default=False,
        verbose_name='Notificação Enviada',
        help_text='Indica se o e-mail de notificação foi enviado com sucesso',
    )
    
    data_notificacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data da Notificação',
    )
    
    class Meta:
        verbose_name = 'Documento do Cliente'
        verbose_name_plural = 'Documentos dos Clientes'
        ordering = ['-data_envio']
        indexes = [
            models.Index(fields=['cliente', '-data_envio']),
            models.Index(fields=['tipo_documento', '-data_envio']),
            models.Index(fields=['notificacao_enviada']),
        ]
    
    def __str__(self):
        cliente_nome = self.cliente.get_full_name() or self.cliente.username
        return f"{self.titulo} - {cliente_nome}"
    
    @property
    def nome_arquivo(self):
        """Retorna apenas o nome do arquivo sem o caminho."""
        if self.arquivo:
            return os.path.basename(self.arquivo.name)
        return "Sem arquivo"
    
    @property
    def tamanho_arquivo(self):
        """Retorna o tamanho do arquivo em formato legível."""
        if self.arquivo:
            size = float(self.arquivo.size)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 B"
    
    @property
    def extensao_arquivo(self):
        """Retorna a extensão do arquivo."""
        if self.arquivo:
            _, ext = os.path.splitext(self.arquivo.name)
            return ext.lower().replace('.', '') if ext else None
        return None
    
    @property
    def tipo_documento_display(self):
        """Retorna o nome legível do tipo de documento."""
        return dict(self.TIPO_DOCUMENTO_CHOICES).get(self.tipo_documento, 'Desconhecido')
    
    @property
    def dias_desde_envio(self):
        """Calcula quantos dias se passaram desde o envio."""
        if self.data_envio:
            delta = timezone.now() - self.data_envio
            return delta.days
        return 0
    
    def marcar_como_visualizado(self):
        """Marca o documento como visualizado pelo cliente."""
        if not self.visualizado:
            self.visualizado = True
            self.data_visualizacao = timezone.now()
            self.save(update_fields=['visualizado', 'data_visualizacao'])
    
    def marcar_notificacao_enviada(self):
        """Marca que a notificação por e-mail foi enviada com sucesso."""
        self.notificacao_enviada = True
        self.data_notificacao = timezone.now()
        self.save(update_fields=['notificacao_enviada', 'data_notificacao'])
    
    def get_absolute_url(self):
        """Retorna a URL para visualizar este documento."""
        return f"/usuarios/documentos/{self.id}/"


def nota_fiscal_cliente_upload_path(instance, filename):
    """
    Define o caminho de upload das notas fiscais enviadas pelos clientes.
    """
    now = timezone.now()
    return f'notas_clientes/{now.year}/{now.month:02d}/cliente_{instance.cliente.id}/{filename}'


class NotaFiscalCliente(models.Model):
    """
    Modelo para Notas Fiscais enviadas pelo cliente para a contabilidade.
    """
    STATUS_CHOICES = [
        ('enviado', 'Enviado'),
        ('em_analise', 'Em Análise'),
        ('processado', 'Processado'),
        ('rejeitado', 'Rejeitado'),
    ]

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notas_fiscais_enviadas_cliente',
        verbose_name='Cliente'
    )
    arquivo = models.FileField(
        upload_to=nota_fiscal_cliente_upload_path, 
        verbose_name='Arquivo'
    )
    descricao = models.CharField(
        max_length=255, 
        verbose_name='Descrição', 
        blank=True
    )
    data_envio = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Data de Envio'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='enviado', 
        verbose_name='Status'
    )

    class Meta:
        verbose_name = 'Nota Fiscal (Cliente)'
        verbose_name_plural = 'Notas Fiscais (Clientes)'
        ordering = ['-data_envio']
        
    def __str__(self):
        return f"NF Enviada - {self.cliente} - {self.data_envio.strftime('%d/%m/%Y')}"
        
    @property
    def nome_arquivo(self):
        if self.arquivo:
            return os.path.basename(self.arquivo.name)
        return "Sem arquivo"
        
    @property
    def tamanho_arquivo(self):
        if self.arquivo:
            size = self.arquivo.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 B"


def boleto_contabilidade_upload_path(instance, filename):
    """
    Define o caminho de upload dos boletos de contabilidade.
    Organiza por ano/mês e ID do cliente.
    """
    from datetime import datetime
    now = datetime.now()
    return f'boletos_contabilidade/{now.year}/{now.month:02d}/cliente_{instance.cliente.id}/{filename}'


class BoletoContabilidade(models.Model):
    """
    Modelo para gerenciamento de Boletos da Mensalidade de Contabilidade.
    Enviados pela equipe do escritório para os clientes.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('vencido', 'Vencido'),
        ('cancelado', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='boletos_contabilidade',
        verbose_name='Cliente',
        help_text='Cliente que receberá o boleto'
    )
    
    referencia = models.CharField(
        max_length=50,
        verbose_name='Mês de Referência',
        help_text='Mês/ano de referência do boleto (ex: Janeiro/2026)'
    )
    
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor',
        help_text='Valor do boleto em reais'
    )
    
    data_vencimento = models.DateField(
        verbose_name='Data de Vencimento',
        help_text='Data de vencimento do boleto'
    )
    
    arquivo_boleto = models.FileField(
        upload_to=boleto_contabilidade_upload_path,
        verbose_name='Arquivo do Boleto',
        help_text='Arquivo PDF do boleto'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name='Status'
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações',
        help_text='Observações internas sobre este boleto'
    )
    
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='boletos_enviados',
        limit_choices_to={'is_staff': True},
        verbose_name='Enviado por'
    )
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Boleto Contabilidade'
        verbose_name_plural = 'Boletos Contabilidade'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Boleto {self.referencia} - {self.cliente.get_full_name() or self.cliente.username}"
    
    @property
    def nome_arquivo(self):
        if self.arquivo_boleto:
            return os.path.basename(self.arquivo_boleto.name)
        return "Sem arquivo"
    
    @property
    def tamanho_arquivo(self):
        if self.arquivo_boleto:
            size = self.arquivo_boleto.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 B"
    
    @property
    def is_vencido(self):
        from datetime import date
        return self.data_vencimento < date.today() and self.status == 'pendente'
