import traceback
import sys
from django.utils.cache import patch_cache_control


class DebugExceptionMiddleware:
    """Middleware para logar todas as exceções não tratadas."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            print("=" * 80, file=sys.stderr)
            print(f"EXCEPTION IN REQUEST: {request.path}", file=sys.stderr)
            print(f"Exception type: {type(e).__name__}", file=sys.stderr)
            print(f"Exception message: {str(e)}", file=sys.stderr)
            print("Traceback:", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print("=" * 80, file=sys.stderr)
            raise
    
    def process_exception(self, request, exception):
        print("=" * 80, file=sys.stderr)
        print(f"PROCESS_EXCEPTION: {request.path}", file=sys.stderr)
        print(f"Exception type: {type(exception).__name__}", file=sys.stderr)
        print(f"Exception message: {str(exception)}", file=sys.stderr)
        print("Traceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        return None


class CacheControlMiddleware:
    """
    Middleware para adicionar headers de cache adequados para diferentes tipos de recursos.
    
    - Arquivos estáticos: cache agressivo (1 ano, immutable)
    - Arquivos de mídia: cache moderado (30 dias)
    - Páginas HTML: sem cache (sempre validar)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)
    
    def process_response(self, request, response):
        # Arquivos estáticos - cache máximo
        if request.path.startswith('/static/'):
            patch_cache_control(
                response,
                max_age=31536000,  # 1 ano
                public=True,
                immutable=True
            )
        
        # Arquivos de mídia - cache moderado
        elif request.path.startswith('/media/'):
            patch_cache_control(
                response,
                max_age=2592000,  # 30 dias
                public=True
            )
        
        # Páginas HTML - sem cache (sempre validar)
        elif response.get('Content-Type', '').startswith('text/html'):
            patch_cache_control(
                response,
                no_cache=True,
                must_revalidate=True,
                max_age=0
            )
        
        return response


class SecurityHeadersMiddleware:
    """
    Middleware para adicionar headers de segurança e performance.
    
    Headers adicionados:
    - X-Content-Type-Options: nosniff (previne MIME sniffing)
    - X-Frame-Options: SAMEORIGIN (previne clickjacking)
    - X-XSS-Protection: 1; mode=block (proteção contra XSS em browsers antigos)
    - Vary: Accept-Encoding (importante para compressão)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)
    
    def process_response(self, request, response):
        # Previne MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Proteção contra clickjacking
        if not response.get('X-Frame-Options'):
            response['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Proteção XSS para browsers antigos
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Importante para compressão funcionar corretamente
        if 'Vary' not in response:
            response['Vary'] = 'Accept-Encoding'
        elif 'Accept-Encoding' not in response['Vary']:
            response['Vary'] += ', Accept-Encoding'
        
        return response
