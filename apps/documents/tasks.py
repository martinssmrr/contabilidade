"""
Tasks Celery para envio de e-mails de notificação de documentos.

Este módulo contém todas as tasks assíncronas relacionadas ao
envio de e-mails transacionais.

Características:
- Retry automático em caso de falha
- Logging detalhado
- Desacoplamento da view
- Type hints completos

Autor: Sistema Vetorial
Data: 2025-12-02
"""

from celery import shared_task
from django.utils import timezone
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 1 minuto
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True
)
def enviar_email_notificacao_documento(
    self,
    documento_id: int
) -> bool:
    """
    Task assíncrona para enviar notificação de novo documento.
    
    Esta task é disparada automaticamente quando um novo documento
    é criado via signal. Ela:
    
    1. Busca os dados do documento
    2. Prepara os dados do cliente
    3. Chama o serviço de e-mail
    4. Atualiza o status da notificação
    5. Trata erros com retry automático
    
    Args:
        documento_id: ID do DocumentoCliente criado
        
    Returns:
        bool: True se enviou com sucesso
        
    Raises:
        Retry: Se houver erro, tenta novamente até max_retries
    """
    try:
        # Import local para evitar circular imports
        from apps.documents.models import DocumentoCliente
        from apps.services.email_service import notificar_novo_documento
        
        # Buscar documento
        try:
            documento = DocumentoCliente.objects.select_related('cliente', 'enviado_por').get(id=documento_id)
        except DocumentoCliente.DoesNotExist:
            logger.error(f"Documento ID {documento_id} não encontrado")
            return False
        
        # Extrair dados do cliente
        cliente = documento.cliente
        cliente_nome = cliente.get_full_name() or cliente.username
        cliente_email = cliente.email
        
        if not cliente_email:
            logger.error(f"Cliente {cliente.username} não possui e-mail cadastrado")
            return False
        
        # Preparar dados do documento
        tipo_documento = documento.tipo_documento_display
        titulo_documento = documento.titulo
        data_envio = documento.data_envio.strftime('%d/%m/%Y às %H:%M')
        descricao = documento.descricao
        
        # Enviar e-mail
        logger.info(f"Enviando notificação de documento para {cliente_email}")
        
        sucesso = notificar_novo_documento(
            cliente_nome=cliente_nome,
            cliente_email=cliente_email,
            tipo_documento=tipo_documento,
            titulo_documento=titulo_documento,
            data_envio=data_envio,
            descricao=descricao,
            documento_id=documento.id
        )
        
        # Atualizar status da notificação no documento
        if sucesso:
            documento.marcar_notificacao_enviada()
            logger.info(f"Notificação enviada com sucesso para {cliente_email}")
        else:
            logger.error(f"Falha ao enviar notificação para {cliente_email}")
            # Tentar novamente
            raise Exception("Falha no envio do e-mail")
        
        return sucesso
        
    except Exception as e:
        logger.error(f"Erro na task de envio de e-mail: {str(e)}")
        # Celery vai tentar novamente automaticamente
        raise


@shared_task(bind=True, max_retries=2)
def enviar_email_simples_async(
    self,
    destinatario: str,
    assunto: str,
    mensagem: str,
    html_mensagem: Optional[str] = None
) -> bool:
    """
    Task genérica para envio de e-mails simples.
    
    Args:
        destinatario: E-mail do destinatário
        assunto: Assunto do e-mail
        mensagem: Conteúdo em texto
        html_mensagem: Conteúdo em HTML (opcional)
        
    Returns:
        bool: Sucesso do envio
    """
    try:
        from apps.services.email_service import EmailService
        
        email_service = EmailService()
        sucesso = email_service.enviar_email_simples(
            destinatario=destinatario,
            assunto=assunto,
            mensagem=mensagem,
            html_mensagem=html_mensagem
        )
        
        return sucesso
        
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail simples: {str(e)}")
        raise


@shared_task
def limpar_logs_antigos() -> int:
    """
    Task periódica para limpar logs antigos de notificações.
    
    Pode ser agendada via Celery Beat para rodar diariamente.
    
    Returns:
        int: Número de logs removidos
    """
    try:
        from apps.documents.models import DocumentoCliente
        from datetime import timedelta
        
        # Remover notificações com mais de 90 dias
        data_limite = timezone.now() - timedelta(days=90)
        
        documentos_antigos = DocumentoCliente.objects.filter(
            data_envio__lt=data_limite,
            notificacao_enviada=True
        )
        
        count = documentos_antigos.count()
        logger.info(f"Limpando {count} registros de notificações antigas")
        
        # Aqui você pode arquivar ou deletar conforme necessário
        # Por enquanto, apenas log
        
        return count
        
    except Exception as e:
        logger.error(f"Erro ao limpar logs: {str(e)}")
        return 0


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True
)
def enviar_email_nota_fiscal(self, nota_fiscal_id: int) -> bool:
    """
    Task assíncrona para enviar notificação de Nota Fiscal.
    
    Integração com painel do staff - dispara automaticamente quando
    o staff envia uma NF via /support/dashboard/.
    
    Args:
        nota_fiscal_id: ID da NotaFiscal criada
        
    Returns:
        bool: True se enviou com sucesso
    """
    try:
        from apps.documents.models import NotaFiscal
        from apps.services.email_service import EmailService
        
        nota_fiscal = NotaFiscal.objects.select_related('cliente', 'enviado_por').get(id=nota_fiscal_id)
        
        cliente = nota_fiscal.cliente
        cliente_nome = cliente.get_full_name() or cliente.username
        cliente_email = cliente.email
        
        if not cliente_email:
            logger.error(f"Cliente {cliente.username} não possui e-mail")
            return False
        
        # Enviar e-mail
        email_service = EmailService()
        sucesso = email_service.enviar_email_com_template(
            destinatario=cliente_email,
            assunto='📄 Nova Nota Fiscal Disponível',
            template_html='emails/notificacao_documento.html',
            contexto={
                'cliente_nome': cliente_nome,
                'tipo_documento': 'Nota Fiscal',
                'titulo_documento': f'Nota Fiscal - {nota_fiscal.data_upload.strftime("%d/%m/%Y")}',
                'data_envio': nota_fiscal.data_upload.strftime('%d/%m/%Y às %H:%M'),
                'descricao': nota_fiscal.observacoes or 'Sua nota fiscal está disponível para visualização.',
                'url_documentos': f'{email_service.url_login}/documentos/',
                'url_login': email_service.url_login,
                'email_suporte': email_service.email_suporte,
            }
        )
        
        if sucesso:
            logger.info(f"Notificação de NF enviada para {cliente_email}")
        else:
            logger.error(f"Falha ao enviar notificação de NF para {cliente_email}")
            raise Exception("Falha no envio do e-mail")
        
        return sucesso
        
    except Exception as e:
        logger.error(f"Erro na task de notificação de NF: {str(e)}")
        raise


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True
)
def enviar_email_documento_empresa(self, documento_id: int) -> bool:
    """
    Task assíncrona para enviar notificação de Documento da Empresa.
    
    Integração com painel do staff - dispara automaticamente quando
    o staff envia um documento via /support/dashboard/.
    
    Args:
        documento_id: ID do DocumentoEmpresa criado
        
    Returns:
        bool: True se enviou com sucesso
    """
    try:
        from apps.documents.models import DocumentoEmpresa
        from apps.services.email_service import EmailService
        
        documento = DocumentoEmpresa.objects.select_related('cliente', 'enviado_por').get(id=documento_id)
        
        cliente = documento.cliente
        cliente_nome = cliente.get_full_name() or cliente.username
        cliente_email = cliente.email
        
        if not cliente_email:
            logger.error(f"Cliente {cliente.username} não possui e-mail")
            return False
        
        # Enviar e-mail
        email_service = EmailService()
        sucesso = email_service.enviar_email_com_template(
            destinatario=cliente_email,
            assunto=f'📄 Novo Documento: {documento.titulo}',
            template_html='emails/notificacao_documento.html',
            contexto={
                'cliente_nome': cliente_nome,
                'tipo_documento': documento.get_categoria_display(),
                'titulo_documento': documento.titulo,
                'data_envio': documento.data_upload.strftime('%d/%m/%Y às %H:%M'),
                'descricao': documento.descricao or f'Um novo documento ({documento.get_categoria_display()}) está disponível para você.',
                'url_documentos': f'{email_service.url_login}/documentos/',
                'url_login': email_service.url_login,
                'email_suporte': email_service.email_suporte,
            }
        )
        
        if sucesso:
            logger.info(f"Notificação de Documento Empresa enviada para {cliente_email}")
        else:
            logger.error(f"Falha ao enviar notificação de Documento Empresa para {cliente_email}")
            raise Exception("Falha no envio do e-mail")
        
        return sucesso
        
    except Exception as e:
        logger.error(f"Erro na task de notificação de Documento Empresa: {str(e)}")
        raise


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True
)
def enviar_email_certidao_negativa(self, certidao_id: int) -> bool:
    """
    Task assíncrona para enviar notificação de Certidão Negativa.
    
    Integração com painel do staff - dispara automaticamente quando
    o staff envia uma certidão via /support/dashboard/.
    
    Args:
        certidao_id: ID da CertidaoNegativa criada
        
    Returns:
        bool: True se enviou com sucesso
    """
    try:
        from apps.users.models import CertidaoNegativa
        from apps.services.email_service import EmailService
        
        certidao = CertidaoNegativa.objects.select_related('cliente').get(id=certidao_id)
        
        cliente = certidao.cliente
        cliente_nome = cliente.get_full_name() or cliente.username
        cliente_email = cliente.email
        
        if not cliente_email:
            logger.error(f"Cliente {cliente.username} não possui e-mail")
            return False
        
        # Enviar e-mail
        email_service = EmailService()
        sucesso = email_service.enviar_email_com_template(
            destinatario=cliente_email,
            assunto=f'📄 Nova Certidão: {certidao.get_tipo_display()}',
            template_html='emails/notificacao_documento.html',
            contexto={
                'cliente_nome': cliente_nome,
                'tipo_documento': f'Certidão {certidao.get_tipo_display()}',
                'titulo_documento': f'Certidão {certidao.get_tipo_display()} - Status: {certidao.get_status_display()}',
                'data_envio': certidao.data_envio.strftime('%d/%m/%Y às %H:%M'),
                'descricao': f'Sua certidão {certidao.get_tipo_display().lower()} está disponível para download.',
                'url_documentos': f'{email_service.url_login}/documentos/',
                'url_login': email_service.url_login,
                'email_suporte': email_service.email_suporte,
            }
        )
        
        if sucesso:
            logger.info(f"Notificação de Certidão enviada para {cliente_email}")
        else:
            logger.error(f"Falha ao enviar notificação de Certidão para {cliente_email}")
            raise Exception("Falha no envio do e-mail")
        
        return sucesso
        
    except Exception as e:
        logger.error(f"Erro na task de notificação de Certidão: {str(e)}")
        raise
