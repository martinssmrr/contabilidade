"""
Middleware personalizado para otimizações de performance
"""
from django.utils.cache import patch_cache_control
from django.utils.deprecation import MiddlewareMixin


class CacheControlMiddleware(MiddlewareMixin):
    """
    Adiciona headers de cache para arquivos estáticos e páginas
    """
    def process_response(self, request, response):
        # Cache para arquivos estáticos
        if request.path.startswith('/static/'):
            # Cache por 1 ano para arquivos estáticos
            patch_cache_control(response, max_age=31536000, public=True, immutable=True)
        
        # Cache para imagens de media
        elif request.path.startswith('/media/'):
            # Cache por 30 dias para arquivos de media
            patch_cache_control(response, max_age=2592000, public=True)
        
        # Cache para páginas HTML (mais curto)
        elif response.get('Content-Type', '').startswith('text/html'):
            # Sem cache para HTML por padrão (pode ser ajustado por view)
            if not response.has_header('Cache-Control'):
                patch_cache_control(response, no_cache=True, must_revalidate=True)
        
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Adiciona headers de segurança e performance
    """
    def process_response(self, request, response):
        # Headers de segurança
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Habilitar compressão
        if not response.has_header('Vary'):
            response['Vary'] = 'Accept-Encoding'
        
        return response
