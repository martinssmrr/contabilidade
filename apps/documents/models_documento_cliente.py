"""
Modelo para Documentos de Clientes com notificação automática por e-mail.

Este módulo implementa o modelo DocumentoCliente que permite ao staff
enviar documentos para clientes com notificação automática por e-mail.

Seguindo princípios LGPD:
- Documentos não são anexados ao e-mail
- Apenas notificação é enviada
- Cliente acessa documento na área logada

Autor: Sistema Vetorial
Data: 2025-12-02
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from typing import Optional
import os


def documento_cliente_upload_path(instance: 'DocumentoCliente', filename: str) -> str:
    """
    Define o caminho de upload dos documentos de clientes.
    
    Organiza por:
    - Ano/Mês do envio
    - ID do cliente
    - Nome original do arquivo
    
    Args:
        instance: Instância do modelo DocumentoCliente
        filename: Nome do arquivo original
        
    Returns:
        str: Caminho completo para upload
        
    Example:
        'documentos_clientes/2025/12/cliente_15/contrato_social.pdf'
    """
    now = timezone.now()
    return f'documentos_clientes/{now.year}/{now.month:02d}/cliente_{instance.cliente.id}/{filename}'


class DocumentoCliente(models.Model):
    """
    Modelo para gerenciamento de documentos enviados pelo staff aos clientes.
    
    Este modelo implementa:
    - Upload de documentos pela equipe interna
    - Vinculação com cliente específico
    - Categorização por tipo de documento
    - Tracking de quem enviou e quando
    - Notificação automática por e-mail (via signal)
    
    Attributes:
        cliente: Usuário (cliente) que receberá o documento
        arquivo: Arquivo físico do documento
        tipo_documento: Categoria do documento (contrato, certidão, etc)
        titulo: Título descritivo do documento
        descricao: Descrição adicional (opcional)
        enviado_por: Staff que fez o upload
        data_envio: Data/hora automática do envio
        visualizado: Se o cliente já visualizou
        data_visualizacao: Data/hora da primeira visualização
        notificacao_enviada: Se o e-mail foi enviado com sucesso
        data_notificacao: Data/hora do envio do e-mail
    """
    
    # Tipos de documentos disponíveis
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
    
    # === CAMPOS PRINCIPAIS ===
    
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documentos_recebidos',
        verbose_name='Cliente',
        help_text='Cliente que receberá este documento',
        limit_choices_to={'is_staff': False},  # Apenas clientes, não staff
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
        help_text='Título descritivo do documento (ex: Contrato Social - Alteração 2025)',
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição',
        help_text='Descrição adicional ou observações sobre o documento (opcional)',
    )
    
    # === CAMPOS DE CONTROLE ===
    
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
        help_text='Data e hora em que o documento foi enviado',
        db_index=True,
    )
    
    # === CAMPOS DE VISUALIZAÇÃO ===
    
    visualizado = models.BooleanField(
        default=False,
        verbose_name='Visualizado',
        help_text='Indica se o cliente já visualizou este documento',
    )
    
    data_visualizacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Visualização',
        help_text='Data e hora da primeira visualização pelo cliente',
    )
    
    # === CAMPOS DE NOTIFICAÇÃO ===
    
    notificacao_enviada = models.BooleanField(
        default=False,
        verbose_name='Notificação Enviada',
        help_text='Indica se o e-mail de notificação foi enviado com sucesso',
    )
    
    data_notificacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data da Notificação',
        help_text='Data e hora do envio do e-mail de notificação',
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
    
    def __str__(self) -> str:
        """Representação em string do documento."""
        cliente_nome = self.cliente.get_full_name() or self.cliente.username
        return f"{self.titulo} - {cliente_nome}"
    
    # === PROPERTIES ===
    
    @property
    def nome_arquivo(self) -> str:
        """
        Retorna apenas o nome do arquivo sem o caminho.
        
        Returns:
            str: Nome do arquivo ou "Sem arquivo"
        """
        if self.arquivo:
            return os.path.basename(self.arquivo.name)
        return "Sem arquivo"
    
    @property
    def tamanho_arquivo(self) -> str:
        """
        Retorna o tamanho do arquivo em formato legível.
        
        Returns:
            str: Tamanho formatado (ex: "2.5 MB")
        """
        if self.arquivo:
            size = float(self.arquivo.size)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 B"
    
    @property
    def extensao_arquivo(self) -> Optional[str]:
        """
        Retorna a extensão do arquivo.
        
        Returns:
            Optional[str]: Extensão sem o ponto (ex: 'pdf', 'docx') ou None
        """
        if self.arquivo:
            _, ext = os.path.splitext(self.arquivo.name)
            return ext.lower().replace('.', '') if ext else None
        return None
    
    @property
    def tipo_documento_display(self) -> str:
        """
        Retorna o nome legível do tipo de documento.
        
        Returns:
            str: Nome formatado do tipo
        """
        return dict(self.TIPO_DOCUMENTO_CHOICES).get(self.tipo_documento, 'Desconhecido')
    
    @property
    def dias_desde_envio(self) -> int:
        """
        Calcula quantos dias se passaram desde o envio.
        
        Returns:
            int: Número de dias
        """
        if self.data_envio:
            delta = timezone.now() - self.data_envio
            return delta.days
        return 0
    
    # === MÉTODOS ===
    
    def marcar_como_visualizado(self) -> None:
        """
        Marca o documento como visualizado pelo cliente.
        
        Atualiza os campos:
        - visualizado = True
        - data_visualizacao = agora (se ainda não foi definida)
        """
        if not self.visualizado:
            self.visualizado = True
            self.data_visualizacao = timezone.now()
            self.save(update_fields=['visualizado', 'data_visualizacao'])
    
    def marcar_notificacao_enviada(self) -> None:
        """
        Marca que a notificação por e-mail foi enviada com sucesso.
        
        Atualiza os campos:
        - notificacao_enviada = True
        - data_notificacao = agora
        """
        self.notificacao_enviada = True
        self.data_notificacao = timezone.now()
        self.save(update_fields=['notificacao_enviada', 'data_notificacao'])
    
    def get_absolute_url(self) -> str:
        """
        Retorna a URL para visualizar este documento.
        
        Returns:
            str: URL da área do cliente para ver documentos
        """
        # TODO: Ajustar para a URL real da área do cliente
        return f"/usuarios/documentos/{self.id}/"
