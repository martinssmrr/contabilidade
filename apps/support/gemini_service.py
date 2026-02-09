"""
Serviço de Atendente IA usando Google Gemini
Vetorial Contabilidade
"""
import os
import logging

logger = logging.getLogger(__name__)

# Contexto do sistema para o assistente
SYSTEM_PROMPT = """Você é a Vitória, assistente virtual da Vetorial Contabilidade, uma empresa de contabilidade online especializada em MEI, ME e pequenas empresas.

## Sobre a Vetorial Contabilidade:
- Empresa de contabilidade 100% online
- Especializada em MEI, Microempresas e Empresas de Pequeno Porte
- Oferece serviços de abertura de empresa, contabilidade mensal, troca de contador, declaração de IR
- Atendimento humanizado e tecnologia moderna
- Localizada em Belo Horizonte, MG, mas atende todo o Brasil

## Serviços oferecidos:
1. **Abertura de Empresa** - MEI, ME, LTDA, EIRELI (a partir de R$ 49,90/mês)
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
- E-mail: contato@vetorialcontabilidade.com.br
- Site: vetorialcontabilidade.com.br

## Regras de atendimento:
1. Seja sempre cordial, profissional e empática
2. Use linguagem clara e acessível (evite jargões técnicos complexos)
3. Responda de forma objetiva, mas completa
4. Se não souber algo específico, oriente o cliente a entrar em contato por WhatsApp
5. Incentive o cliente a conhecer os serviços da Vetorial
6. Nunca invente informações sobre valores, prazos ou procedimentos legais específicos
7. Para questões muito específicas de contabilidade, sugira agendar uma consulta com um contador
8. Use emojis com moderação para tornar a conversa mais amigável

## Formato das respostas:
- Seja conciso (máximo 3-4 parágrafos curtos)
- Use bullet points quando listar informações
- Sempre finalize oferecendo ajuda adicional
"""


class GeminiService:
    """Serviço para interação com a API do Google Gemini"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', '')
        self.model = None
        self.chat = None
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                
                # Configuração de segurança mais permissiva para atendimento
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
                ]
                
                # Configuração de geração
                generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 500,
                }
                
                self.model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash-latest",
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    system_instruction=SYSTEM_PROMPT
                )
                
                logger.info("Gemini client inicializado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao inicializar Gemini client: {e}")
    
    def is_available(self):
        """Verifica se o serviço está disponível"""
        return self.model is not None and bool(self.api_key)
    
    def get_response(self, user_message: str, conversation_history: list = None) -> str:
        """
        Obtém uma resposta do assistente IA.
        
        Args:
            user_message: Mensagem do usuário
            conversation_history: Lista de mensagens anteriores [{"role": "user/model", "content": "..."}]
        
        Returns:
            Resposta do assistente
        """
        import time
        
        if not self.is_available():
            logger.warning("Gemini não está disponível")
            return "Desculpe, o atendente virtual está temporariamente indisponível. Por favor, entre em contato pelo WhatsApp (11) 3164-2284."
        
        max_retries = 3
        retry_delay = 2  # segundos
        
        for attempt in range(max_retries):
            try:
                # Construir histórico de chat para o Gemini
                history = []
                if conversation_history:
                    for msg in conversation_history[-10:]:  # Últimas 10 mensagens
                        role = "model" if msg.get("role") == "assistant" else "user"
                        history.append({
                            "role": role,
                            "parts": [msg.get("content", "")]
                        })
                
                # Iniciar chat com histórico
                chat = self.model.start_chat(history=history)
                
                # Enviar mensagem e obter resposta
                response = chat.send_message(user_message)
                
                assistant_message = response.text.strip()
                
                logger.info(f"Gemini resposta gerada com sucesso")
                
                return assistant_message
            
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Erro ao obter resposta do Gemini (tentativa {attempt + 1}): {e}")
                
                # Se for rate limit, esperar e tentar novamente
                if ('quota' in error_msg.lower() or '429' in error_msg or 'resource_exhausted' in error_msg.lower()) and attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)  # Backoff exponencial simples
                    logger.info(f"Rate limit atingido, aguardando {wait_time}s antes de tentar novamente...")
                    time.sleep(wait_time)
                    continue
                
                # Tratar erros específicos
                if 'quota' in error_msg.lower() or '429' in error_msg or 'resource_exhausted' in error_msg.lower():
                    return "Estou processando muitas mensagens no momento. ⏳ Por favor, aguarde alguns segundos e tente novamente!"
                elif 'invalid' in error_msg.lower() or '401' in error_msg or '403' in error_msg:
                    return "Atendente virtual temporariamente indisponível. Entre em contato pelo WhatsApp (11) 3164-2284."
                elif 'blocked' in error_msg.lower() or 'safety' in error_msg.lower():
                    return "Desculpe, não posso responder a essa pergunta. Por favor, reformule ou entre em contato pelo WhatsApp (11) 3164-2284."
                else:
                    return "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente ou entre em contato pelo WhatsApp (11) 3164-2284."
        
        # Se chegou aqui sem retornar, algo deu errado
        return "Desculpe, não consegui processar sua mensagem. Tente novamente em alguns segundos."
    
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
gemini_service = GeminiService()
