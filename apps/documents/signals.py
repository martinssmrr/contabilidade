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


@receiver(post_save, sender='documents.DocumentoCliente')
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


# Registrar o AppConfig para garantir que signals sejam carregados
def register_signals() -> None:
    """
    Função auxiliar para registrar todos os signals.
    
    Chamada no apps.py ready() method.
    """
    logger.info("Signals de notificação de documentos registrados")
