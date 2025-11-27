from django.db import models
from django.conf import settings
import os

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
