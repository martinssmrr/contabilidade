"""
Serviço de Envio de E-mails - Contabilidade Vetorial

Este módulo implementa o serviço de envio de e-mails transacionais
de forma desacoplada e reutilizável.

Características:
- Desacoplado do provedor de e-mail
- Suporte a templates HTML
- Logging de erros
- Type hints completos
- Configurável via settings

Autor: Sistema Vetorial
Data: 2025-12-02
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from typing import Dict, List, Optional, Any
import logging

# Configurar logger
logger = logging.getLogger(__name__)


class EmailService:
    """
    Serviço centralizado para envio de e-mails.
    
    Este serviço abstrai a lógica de envio de e-mails e permite:
    - Envio de e-mails HTML com fallback em texto
    - Templates reutilizáveis
    - Logging de erros
    - Configuração centralizada
    
    Example:
        >>> email_service = EmailService()
        >>> email_service.enviar_notificacao_documento(
        ...     cliente_nome="João Silva",
        ...     cliente_email="joao@example.com",
        ...     tipo_documento="Contrato Social",
        ...     titulo_documento="Contrato Social 2025",
        ...     data_envio="02/12/2025"
        ... )
    """
    
    def __init__(self):
        """Inicializa o serviço com configurações do Django."""
        self.remetente = settings.EMAIL_HOST_USER
        self.nome_empresa = "Contabilidade Vetorial"
        self.url_login = settings.SITE_URL + "/usuarios/login/"
        self.url_documentos = settings.SITE_URL + "/usuarios/documentos/"
        self.email_suporte = "contabilidadevetorial@gmail.com"
    
    def enviar_email_simples(
        self,
        destinatario: str,
        assunto: str,
        mensagem: str,
        html_mensagem: Optional[str] = None
    ) -> bool:
        """
        Envia um e-mail simples (texto ou HTML).
        
        Args:
            destinatario: E-mail do destinatário
            assunto: Assunto do e-mail
            mensagem: Conteúdo em texto puro
            html_mensagem: Conteúdo em HTML (opcional)
            
        Returns:
            bool: True se enviou com sucesso, False caso contrário
        """
        try:
            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=self.remetente,
                recipient_list=[destinatario],
                html_message=html_mensagem,
                fail_silently=False,
            )
            logger.info(f"E-mail enviado com sucesso para {destinatario}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail para {destinatario}: {str(e)}")
            return False
    
    def enviar_email_com_template(
        self,
        destinatario: str,
        assunto: str,
        template_html: str,
        contexto: Dict[str, Any],
        template_texto: Optional[str] = None
    ) -> bool:
        """
        Envia e-mail usando templates Django.
        
        Args:
            destinatario: E-mail do destinatário
            assunto: Assunto do e-mail
            template_html: Caminho do template HTML
            contexto: Dicionário com variáveis do template
            template_texto: Caminho do template texto (opcional)
            
        Returns:
            bool: True se enviou com sucesso, False caso contrário
        """
        try:
            # Renderizar HTML
            html_content = render_to_string(template_html, contexto)
            
            # Renderizar texto (ou extrair do HTML)
            if template_texto:
                text_content = render_to_string(template_texto, contexto)
            else:
                text_content = strip_tags(html_content)
            
            # Criar e-mail multipart
            email = EmailMultiAlternatives(
                subject=assunto,
                body=text_content,
                from_email=self.remetente,
                to=[destinatario]
            )
            email.attach_alternative(html_content, "text/html")
            
            # Enviar
            email.send(fail_silently=False)
            
            logger.info(f"E-mail com template enviado para {destinatario}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail com template para {destinatario}: {str(e)}")
            return False
    
    def enviar_notificacao_documento(
        self,
        cliente_nome: str,
        cliente_email: str,
        tipo_documento: str,
        titulo_documento: str,
        data_envio: str,
        descricao: Optional[str] = None,
        documento_id: Optional[int] = None
    ) -> bool:
        """
        Envia notificação de novo documento disponível.
        
        Este método é o principal do módulo e envia um e-mail
        notificando o cliente sobre um novo documento.
        
        IMPORTANTE (LGPD):
        - O documento NÃO é anexado ao e-mail
        - Apenas notificação é enviada
        - Cliente deve fazer login para acessar
        
        Args:
            cliente_nome: Nome completo do cliente
            cliente_email: E-mail do cliente
            tipo_documento: Tipo do documento (ex: "Contrato Social")
            titulo_documento: Título descritivo do documento
            data_envio: Data de envio formatada (ex: "02/12/2025")
            descricao: Descrição adicional (opcional)
            documento_id: ID do documento para link direto (opcional)
            
        Returns:
            bool: True se enviou com sucesso, False caso contrário
            
        Example:
            >>> EmailService().enviar_notificacao_documento(
            ...     cliente_nome="João Silva",
            ...     cliente_email="joao@example.com",
            ...     tipo_documento="Contrato Social",
            ...     titulo_documento="Contrato Social - Alteração 2025",
            ...     data_envio="02/12/2025",
            ...     descricao="Alteração contratual conforme solicitado"
            ... )
        """
        # Montar contexto para o template
        contexto = {
            'cliente_nome': cliente_nome,
            'tipo_documento': tipo_documento,
            'titulo_documento': titulo_documento,
            'data_envio': data_envio,
            'descricao': descricao,
            'url_login': self.url_login,
            'url_documentos': self.url_documentos,
            'email_suporte': self.email_suporte,
            'nome_empresa': self.nome_empresa,
            'ano_atual': '2025',
        }
        
        # Se temos ID do documento, criar URL direta
        if documento_id:
            contexto['url_documento'] = f"{settings.SITE_URL}/usuarios/documentos/{documento_id}/"
        
        # Assunto do e-mail
        assunto = f"📄 Novo documento disponível - {tipo_documento}"
        
        # Enviar usando template
        return self.enviar_email_com_template(
            destinatario=cliente_email,
            assunto=assunto,
            template_html='emails/notificacao_documento.html',
            contexto=contexto
        )
    
    def enviar_multiplos_emails(
        self,
        destinatarios: List[str],
        assunto: str,
        mensagem: str,
        html_mensagem: Optional[str] = None
    ) -> Dict[str, bool]:
        """
        Envia o mesmo e-mail para múltiplos destinatários.
        
        Args:
            destinatarios: Lista de e-mails
            assunto: Assunto do e-mail
            mensagem: Conteúdo em texto
            html_mensagem: Conteúdo em HTML (opcional)
            
        Returns:
            Dict[str, bool]: Mapa de destinatário -> sucesso
        """
        resultados = {}
        
        for destinatario in destinatarios:
            sucesso = self.enviar_email_simples(
                destinatario=destinatario,
                assunto=assunto,
                mensagem=mensagem,
                html_mensagem=html_mensagem
            )
            resultados[destinatario] = sucesso
        
        return resultados


# === FUNÇÕES DE CONVENIÊNCIA ===

def notificar_novo_documento(
    cliente_nome: str,
    cliente_email: str,
    tipo_documento: str,
    titulo_documento: str,
    data_envio: str,
    descricao: Optional[str] = None,
    documento_id: Optional[int] = None
) -> bool:
    """
    Função de conveniência para enviar notificação de documento.
    
    Esta é a função principal que deve ser chamada pelas tasks do Celery.
    
    Args:
        cliente_nome: Nome do cliente
        cliente_email: E-mail do cliente
        tipo_documento: Tipo do documento
        titulo_documento: Título do documento
        data_envio: Data formatada
        descricao: Descrição (opcional)
        documento_id: ID do documento (opcional)
        
    Returns:
        bool: Sucesso do envio
    """
    email_service = EmailService()
    return email_service.enviar_notificacao_documento(
        cliente_nome=cliente_nome,
        cliente_email=cliente_email,
        tipo_documento=tipo_documento,
        titulo_documento=titulo_documento,
        data_envio=data_envio,
        descricao=descricao,
        documento_id=documento_id
    )
