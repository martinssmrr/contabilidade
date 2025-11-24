"""
Serviço de integração com Evolution API para envio de mensagens WhatsApp.
"""
import requests
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class EvolutionAPIService:
    """
    Classe para gerenciar comunicação com a Evolution API.
    """
    
    def __init__(self):
        """
        Inicializa o serviço com as credenciais da Evolution API.
        As credenciais devem ser configuradas nas variáveis de ambiente.
        """
        self.base_url = os.getenv('EVOLUTION_API_URL', '')
        self.api_key = os.getenv('EVOLUTION_API_KEY', '')
        self.instance_name = os.getenv('EVOLUTION_INSTANCE_NAME', '')
        self.sender_number = os.getenv('WHATSAPP_SENDER_NUMBER', '5561998311920')
        
        # Evolution API removida do projeto - usando wa.me para WhatsApp
        self.enabled = False
        if not all([self.base_url, self.api_key, self.instance_name]):
            logger.info('Evolution API desabilitada. WhatsApp via wa.me apenas.')
    
    def format_phone_number(self, phone):
        """
        Formata o número de telefone para o padrão da Evolution API.
        
        Args:
            phone (str): Número de telefone com DDD (ex: (61) 99831-1920 ou 61998311920)
        
        Returns:
            str: Número formatado no padrão internacional (ex: 5561998311920)
        """
        # Remove caracteres não numéricos
        phone_digits = ''.join(filter(str.isdigit, phone))
        
        # Se não começa com 55, adiciona o código do Brasil
        if not phone_digits.startswith('55'):
            phone_digits = f'55{phone_digits}'
        
        # Adiciona @s.whatsapp.net (formato Evolution API)
        return f'{phone_digits}@s.whatsapp.net'
    
    def send_text(self, phone, name='Cliente'):
        """
        Envia uma mensagem de texto de boas-vindas para o cliente.
        DESABILITADO - Evolution API foi removida.
        
        Args:
            phone (str): Número de telefone do destinatário
            name (str): Nome do destinatário
        
        Returns:
            dict: Erro informando que o serviço foi desabilitado
        """
        logger.info('WhatsApp API desabilitada. Use wa.me para contato direto.')
        return {
            'success': False,
            'error': 'Serviço desabilitado',
            'message': 'WhatsApp API foi removida. Use links wa.me para contato direto.'
        }
        
        # Formata o número de telefone
        formatted_phone = self.format_phone_number(phone)
        
        # Monta a mensagem personalizada
        message = (
            f"Olá, {name}! 👋\n\n"
            f"Recebemos sua mensagem e em breve um de nossos especialistas entrará em contato. "
            f"Obrigado pelo seu interesse!\n\n"
            f"*Contabilidade Vetorial*\n"
            f"📞 {self.sender_number}"
        )
        
        # URL do endpoint de envio de mensagem
        url = f"{self.base_url}/message/sendText/{self.instance_name}"
        
        # Headers da requisição
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        
        # Payload da requisição
        payload = {
            'number': formatted_phone,
            'text': message,
            'delay': 1200  # Delay de 1.2 segundos para parecer mais natural
        }
        
        try:
            logger.info(f'Enviando mensagem WhatsApp para {formatted_phone}')
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            response.raise_for_status()
            
            logger.info(f'Mensagem enviada com sucesso para {formatted_phone}')
            
            return {
                'success': True,
                'response': response.json(),
                'status_code': response.status_code
            }
        
        except requests.exceptions.Timeout:
            logger.error(f'Timeout ao enviar mensagem para {formatted_phone}')
            return {
                'success': False,
                'error': 'Timeout na requisição'
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f'Erro ao enviar mensagem para {formatted_phone}: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None)
            }
        
        except Exception as e:
            logger.error(f'Erro inesperado ao enviar mensagem: {str(e)}')
            return {
                'success': False,
                'error': f'Erro inesperado: {str(e)}'
            }
    
    def send_custom_message(self, phone, message):
        """
        Envia mensagem customizada para um número.
        DESABILITADO - Evolution API foi removida.
        
        Args:
            phone (str): Número de telefone do destinatário
            message (str): Mensagem a ser enviada
        
        Returns:
            dict: Erro informando que o serviço foi desabilitado
        """
        logger.info('WhatsApp API desabilitada. Use wa.me para contato direto.')
        return {
            'success': False,
            'error': 'Serviço desabilitado',
            'message': 'WhatsApp API foi removida. Use links wa.me para contato direto.'
        }
        
        formatted_phone = self.format_phone_number(phone)
        url = f"{self.base_url}/message/sendText/{self.instance_name}"
        
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        
        payload = {
            'number': formatted_phone,
            'text': message,
            'delay': 1200
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            response.raise_for_status()
            
            return {
                'success': True,
                'response': response.json(),
                'status_code': response.status_code
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f'Erro ao enviar mensagem customizada: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_connection(self):
        """
        Verifica se a conexão com a Evolution API está funcionando.
        DESABILITADO - Evolution API foi removida.
        
        Returns:
            dict: Erro informando que o serviço foi desabilitado
        """
        logger.info('WhatsApp API desabilitada.')
        return {
            'success': False,
            'error': 'Serviço desabilitado',
            'message': 'WhatsApp API foi removida do projeto.'
        }
        
        url = f"{self.base_url}/instance/connectionState/{self.instance_name}"
        
        headers = {
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return {
                'success': True,
                'status': response.json()
            }
        
        except Exception as e:
            logger.error(f'Erro ao verificar conexão: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }


# Instância global do serviço
whatsapp_service = EvolutionAPIService()
