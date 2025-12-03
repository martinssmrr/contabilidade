"""
Signals para notificação automática de documentos.

Este módulo implementa signals Django para disparar ações automáticas
quando um documento é criado/atualizado.

Princípios:
- Desacoplamento total da view
- Processamento assíncrono via Celery
- Logging de todas as operações
- Type hints completos

Autor: Sistema Vetorial
Data: 2025-12-02
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import Any
import logging

logger = logging.getLogger(__name__)


# Conectar signals após importações evitar problemas de circular import
def connect_signals():
    """
    Conecta os signals aos modelos.
    Chamado no apps.py ready() method após todos os modelos estarem carregados.
    """
    from apps.documents.models import NotaFiscal, DocumentoEmpresa, DocumentoCliente
    from apps.users.models import CertidaoNegativa
    
    post_save.connect(notificar_cliente_novo_documento, sender=DocumentoCliente)
    post_save.connect(notificar_cliente_nota_fiscal, sender=NotaFiscal)
    post_save.connect(notificar_cliente_documento_empresa, sender=DocumentoEmpresa)
    post_save.connect(notificar_cliente_certidao_negativa, sender=CertidaoNegativa)
    
    print("🔗 Signals conectados aos modelos!")
    logger.info("Signals conectados aos modelos!")


# @receiver(post_save, sender='documents.DocumentoCliente')  # Removido decorator
def notificar_cliente_novo_documento(
    sender: Any,
    instance: 'DocumentoCliente',
    created: bool,
    **kwargs
) -> None:
    """
    Signal que dispara notificação por e-mail quando um novo documento é criado.
    
    Este signal é ativado automaticamente após o save() de um DocumentoCliente.
    Ele agenda uma task assíncrona no Celery para enviar o e-mail sem bloquear
    a resposta HTTP.
    
    Args:
        sender: Classe do modelo (DocumentoCliente)
        instance: Instância do documento criado
        created: True se é uma criação, False se é atualização
        **kwargs: Argumentos adicionais do signal
        
    Behavior:
        - Só executa se for criação (created=True)
        - Só envia se o cliente tiver e-mail
        - Só envia uma vez (verifica notificacao_enviada)
        - Dispara task assíncrona do Celery
        - Log de todas as ações
    """
    # Só processar criações, não atualizações
    if not created:
        logger.debug(f"Documento ID {instance.id} atualizado, signal ignorado")
        return
    
    # Verificar se já foi enviada notificação (precaução)
    if instance.notificacao_enviada:
        logger.info(f"Notificação já enviada para documento ID {instance.id}, ignorando")
        return
    
    # Verificar se o cliente tem e-mail
    if not instance.cliente.email:
        logger.warning(
            f"Cliente {instance.cliente.username} não possui e-mail cadastrado. "
            f"Notificação do documento ID {instance.id} não será enviada."
        )
        return
    
    try:
        # Importar task aqui para evitar circular imports
        from apps.documents.tasks import enviar_email_notificacao_documento
        
        # Disparar task assíncrona do Celery
        logger.info(
            f"Agendando envio de notificação para documento ID {instance.id} "
            f"(Cliente: {instance.cliente.username})"
        )
        
        # delay() executa a task de forma assíncrona
        enviar_email_notificacao_documento.delay(instance.id)
        
        logger.info(f"Task agendada com sucesso para documento ID {instance.id}")
        
    except Exception as e:
        logger.error(
            f"Erro ao agendar task de e-mail para documento ID {instance.id}: {str(e)}"
        )
        # Não propagar a exceção para não quebrar o save()


# @receiver(post_save, sender='documents.NotaFiscal')  # Removido decorator
def notificar_cliente_nota_fiscal(
    sender: Any,
    instance: 'NotaFiscal',
    created: bool,
    **kwargs
) -> None:
    """
    Signal que dispara notificação por e-mail quando uma Nota Fiscal é enviada.
    
    Integração com o painel do staff (/support/dashboard/)
    Dispara automaticamente quando o staff faz upload de uma NF.
    
    Args:
        sender: Classe do modelo (NotaFiscal)
        instance: Instância da nota fiscal criada
        created: True se é uma criação, False se é atualização
        **kwargs: Argumentos adicionais do signal
    """
    print(f"🚨 SIGNAL NOTA FISCAL DISPARADO! ID: {instance.id}, created: {created}")
    
    if not created:
        print(f"⚠️  Nota Fiscal {instance.id} não é nova (created=False), ignorando")
        logger.debug(f"Nota Fiscal ID {instance.id} atualizada, signal ignorado")
        return
    
    print(f"✅ É nova! Cliente: {instance.cliente.username}, Email: {instance.cliente.email}")
    
    if not instance.cliente.email:
        print(f"❌ Cliente sem e-mail!")
        logger.warning(
            f"Cliente {instance.cliente.username} não possui e-mail. "
            f"Nota Fiscal ID {instance.id} não será notificada."
        )
        return
    
    try:
        print(f"📤 Importando task e agendando...")
        from apps.documents.tasks import enviar_email_nota_fiscal
        
        logger.info(
            f"Agendando notificação de Nota Fiscal ID {instance.id} "
            f"para {instance.cliente.username}"
        )
        print(f"📧 Chamando enviar_email_nota_fiscal.delay({instance.id})")
        
        enviar_email_nota_fiscal.delay(instance.id)
        
        print(f"✅ Task agendada com sucesso!")
        
        logger.info(f"Task de NF agendada com sucesso para ID {instance.id}")
        
    except Exception as e:
        logger.error(
            f"Erro ao agendar notificação de NF ID {instance.id}: {str(e)}"
        )


# @receiver(post_save, sender='documents.DocumentoEmpresa')  # Removido decorator
def notificar_cliente_documento_empresa(
    sender: Any,
    instance: 'DocumentoEmpresa',
    created: bool,
    **kwargs
) -> None:
    """
    Signal que dispara notificação por e-mail quando um Documento da Empresa é enviado.
    
    Integração com o painel do staff (/support/dashboard/)
    Dispara automaticamente quando o staff faz upload de um documento.
    
    Args:
        sender: Classe do modelo (DocumentoEmpresa)
        instance: Instância do documento criado
        created: True se é uma criação, False se é atualização
        **kwargs: Argumentos adicionais do signal
    """
    if not created:
        logger.debug(f"Documento Empresa ID {instance.id} atualizado, signal ignorado")
        return
    
    if not instance.cliente.email:
        logger.warning(
            f"Cliente {instance.cliente.username} não possui e-mail. "
            f"Documento Empresa ID {instance.id} não será notificado."
        )
        return
    
    try:
        from apps.documents.tasks import enviar_email_documento_empresa
        
        logger.info(
            f"Agendando notificação de Documento Empresa ID {instance.id} "
            f"para {instance.cliente.username}"
        )
        
        enviar_email_documento_empresa.delay(instance.id)
        
        logger.info(f"Task de Documento Empresa agendada com sucesso para ID {instance.id}")
        
    except Exception as e:
        logger.error(
            f"Erro ao agendar notificação de Documento Empresa ID {instance.id}: {str(e)}"
        )


# @receiver(post_save, sender='users.CertidaoNegativa')  # Removido decorator
def notificar_cliente_certidao_negativa(
    sender: Any,
    instance: 'CertidaoNegativa',
    created: bool,
    **kwargs
) -> None:
    """
    Signal que dispara notificação por e-mail quando uma Certidão Negativa é enviada.
    
    Integração com o painel do staff (/support/dashboard/)
    Dispara automaticamente quando o staff faz upload de uma certidão.
    
    Args:
        sender: Classe do modelo (CertidaoNegativa)
        instance: Instância da certidão criada
        created: True se é uma criação, False se é atualização
        **kwargs: Argumentos adicionais do signal
    """
    if not created:
        logger.debug(f"Certidão Negativa ID {instance.id} atualizada, signal ignorado")
        return
    
    if not instance.cliente.email:
        logger.warning(
            f"Cliente {instance.cliente.username} não possui e-mail. "
            f"Certidão Negativa ID {instance.id} não será notificada."
        )
        return
    
    try:
        from apps.documents.tasks import enviar_email_certidao_negativa
        
        logger.info(
            f"Agendando notificação de Certidão Negativa ID {instance.id} "
            f"para {instance.cliente.username}"
        )
        
        enviar_email_certidao_negativa.delay(instance.id)
        
        logger.info(f"Task de Certidão agendada com sucesso para ID {instance.id}")
        
    except Exception as e:
        logger.error(
            f"Erro ao agendar notificação de Certidão ID {instance.id}: {str(e)}"
        )


# Registrar o AppConfig para garantir que signals sejam carregados
def register_signals() -> None:
    """
    Função auxiliar para registrar todos os signals.
    
    Chamada no apps.py ready() method.
    """
    connect_signals()  # Conectar signals aos modelos
    print("🔔 Signals de notificação registrados: DocumentoCliente, NotaFiscal, DocumentoEmpresa, CertidaoNegativa")
    logger.info("Signals de notificação registrados: DocumentoCliente, NotaFiscal, DocumentoEmpresa, CertidaoNegativa")
