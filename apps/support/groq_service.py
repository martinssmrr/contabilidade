"""
Serviço de Atendente IA usando Groq (Llama 3)
Vetorial Contabilidade
"""
import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

# Contexto do sistema para o assistente
SYSTEM_PROMPT = """
Você é a Vitória, assistente virtual da Vetorial Contabilidade, uma empresa de contabilidade online especializada em MEI, ME e pequenas empresas.

Sobre a Vetorial Contabilidade:
- Empresa de contabilidade 100% online
- Especializada em MEI, Microempresas e Empresas de Pequeno Porte
- Oferece serviços de abertura de empresa, contabilidade mensal, troca de contador, declaração de IR
- Atendimento humanizado e tecnologia moderna
- Localizada em Belo Horizonte, MG, mas atende todo o Brasil

Serviços oferecidos:
- Abertura de ME, LTDA, EIRELI (com planos a partir de R$ 119,90/mês)
- Abertura de Empresa: MEI (a partir de R$ 49,90/mês)
- Contabilidade Completa: Escrituração, obrigações fiscais, folha de pagamento
- Troca de Contador: Migração simplificada e sem burocracia
- Declaração de Imposto de Renda: IRPF e IRPJ
- Regularização Fiscal: Débitos, certidões, pendências
- Consultoria Empresarial: Planejamento tributário, gestão financeira
- Planos: Preços acessíveis a partir de R$ 49,90/mês para MEI e R$ 119,90/mês para ME

Diferenciais:
- Plataforma online para acompanhar tudo
- Atendimento por WhatsApp
- Preços transparentes e acessíveis
- Equipe especializada e certificada

Contatos:
- WhatsApp: (11) 3164-2284
- E-mail: contato@vetorialcontabilidade.com.br

Regras de atendimento:
- Nunca ensinar o passo a passo ao cliente, sempre direcionar para o WhatsApp (11) 3164-2284.
- Seja sempre cordial, profissional e empática.
- Use linguagem clara e acessível (evite jargões técnicos complexos).
- Responda de forma objetiva, mas completa.
- Se não souber algo específico, oriente o cliente a entrar em contato pelo WhatsApp.
- Incentive o cliente a conhecer os serviços da Vetorial.
- Nunca invente informações sobre valores, prazos ou procedimentos legais específicos.
- Para questões muito específicas de contabilidade, sugira agendar uma consulta com um contador.
- Use emojis com moderação, apenas para tornar a conversa mais amigável.
- Não use * nem ** nas respostas.

Formato das respostas:
- Não use * nem ** nas respostas.
- Seja conciso, com no máximo 3 a 4 parágrafos curtos.
- Sempre finalize oferecendo ajuda adicional, como: "Caso precise de mais informações, estou à disposição!"

"""


class GroqService:
    """Serviço para interação com a API do Groq (Llama 3)"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY', '')
        self.client = None
        self.model = "llama-3.3-70b-versatile"  # Modelo mais capaz e gratuito
        
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info("Groq client inicializado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao inicializar Groq client: {e}")
    
    def is_available(self):
        """Verifica se o serviço está disponível"""
        return self.client is not None and bool(self.api_key)
    
    def get_response(self, user_message: str, conversation_history: list = None) -> str:
        """
        Obtém uma resposta do assistente IA.
        
        Args:
            user_message: Mensagem do usuário
            conversation_history: Lista de mensagens anteriores [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            Resposta do assistente
        """
        if not self.is_available():
            logger.warning("Groq não está disponível")
            return "Desculpe, o atendente virtual está temporariamente indisponível. Por favor, entre em contato pelo WhatsApp (11) 3164-2284."
        
        try:
            # Construir mensagens
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            
            # Adicionar histórico de conversa (últimas 10 mensagens para economizar tokens)
            if conversation_history:
                messages.extend(conversation_history[-10:])
            
            # Adicionar mensagem atual
            messages.append({"role": "user", "content": user_message})
            
            # Fazer chamada à API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
            )
            
            assistant_message = response.choices[0].message.content.strip()
            
            logger.info(f"Groq resposta gerada. Tokens: {response.usage.total_tokens}")
            
            return assistant_message
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Erro ao obter resposta do Groq: {e}")
            
            # Tratar erros específicos
            if 'rate_limit' in error_msg.lower() or '429' in error_msg:
                return "Estou processando muitas mensagens no momento. ⏳ Por favor, aguarde alguns segundos e tente novamente!"
            elif 'invalid' in error_msg.lower() or '401' in error_msg or '403' in error_msg:
                return "Atendente virtual temporariamente indisponível. Entre em contato pelo WhatsApp (11) 3164-2284."
            else:
                return "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente ou entre em contato pelo WhatsApp (11) 3164-2284."
    
    def get_conversation_history_from_session(self, sessao) -> list:
        """
        Extrai o histórico de conversa de uma sessão do chatbot.
        
        Args:
            sessao: Objeto ChatbotSessao
        
        Returns:
            Lista de mensagens formatadas para a API
        """
        from .models import ChatbotMensagem
        
        mensagens = ChatbotMensagem.objects.filter(
            sessao=sessao
        ).order_by('criado_em')[:20]  # Limitar a 20 mensagens
        
        history = []
        for msg in mensagens:
            role = "assistant" if msg.is_bot else "user"
            history.append({
                "role": role,
                "content": msg.conteudo
            })
        
        return history


# Instância singleton do serviço
groq_service = GroqService()
