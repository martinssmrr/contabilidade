"""
Serviço de Atendente IA usando OpenAI GPT
Vetorial Contabilidade
"""
import os
import logging
from openai import OpenAI
from django.conf import settings

logger = logging.getLogger(__name__)

# Contexto do sistema para o assistente
SYSTEM_PROMPT = """Você é a Vitória, assistente virtual da Vetorial Contabilidade, uma empresa de contabilidade online especializada em MEI, ME e pequenas empresas.

## Sobre a Vetorial Contabilidade:
- Empresa de contabilidade 100% online
- Especializada em MEI, Microempresas e Empresas de Pequeno Porte
- Oferece serviços de abertura de empresa, contabilidade mensal, troca de contador, declaração de IR
- Atendimento humanizado e tecnologia moderna
- Localizada em Salvador, BA, mas atende todo o Brasil

## Serviços oferecidos:
1. **Abertura de Empresa** - MEI, ME, LTDA, EIRELI (a partir de R$ 49,90/mês para MEI e R$ 119,90/mês para ME)
2. **Contabilidade Completa** - Escrituração, obrigações fiscais, folha de pagamento
3. **Troca de Contador** - Migração simplificada e sem burocracia
4. **Declaração de Imposto de Renda** - IRPF e IRPJ
5. **Regularização Fiscal** - Débitos, certidões, pendências
6. **Consultoria Empresarial** - Planejamento tributário, gestão financeira

## Diferenciais:
- Plataforma online para acompanhar tudo
- Atendimento por WhatsApp
- Preços transparentes e acessíveis
- Equipe especializada e certificada

## Contatos:
- WhatsApp: (11) 3164-2284
- E-mail: contabilidadevetorial@gmail.com
- Site: vetorialcontabilidade.com.br

## Regras de atendimento:
1. Seja sempre cordial, profissional e empática
2. Use linguagem clara e acessível (evite jargões técnicos complexos)
3. Responda de forma objetiva, mas completa
4. Se não souber algo específico, oriente o cliente a entrar em contato por WhatsApp (11) 3164-2284
5. Incentive o cliente a conhecer os serviços da Vetorial
6. Nunca invente informações sobre valores, prazos ou procedimentos legais específicos
7. Para questões muito específicas de contabilidade, sugira agendar uma consulta com um contador
8. Use emojis com moderação para tornar a conversa mais amigável

## Formato das respostas:
- Seja conciso (máximo 3-4 parágrafos curtos)
- Use bullet points quando listar informações
- Sempre finalize oferecendo ajuda adicional
"""


class OpenAIService:
    """Serviço para interação com a API da OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        self.client = None
        self.model = "gpt-4o-mini"  # Modelo mais econômico e eficiente
        
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client inicializado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao inicializar OpenAI client: {e}")
    
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
            logger.warning("OpenAI não está disponível")
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
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            assistant_message = response.choices[0].message.content.strip()
            
            logger.info(f"OpenAI resposta gerada. Tokens: {response.usage.total_tokens}")
            
            return assistant_message
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Erro ao obter resposta da OpenAI: {e}")
            
            # Tratar erros específicos
            if 'insufficient_quota' in error_msg or '429' in error_msg:
                return "No momento nosso atendente virtual está em manutenção. 🔧 Por favor, entre em contato pelo WhatsApp (11) 3164-2284 ou selecione uma das perguntas rápidas!"
            elif 'invalid_api_key' in error_msg or '401' in error_msg:
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
openai_service = OpenAIService()
