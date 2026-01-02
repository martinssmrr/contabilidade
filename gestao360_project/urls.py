"""
URL configuration for vetorial_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.http import JsonResponse
from apps.testimonials.models import Testimonial
from apps.services.views import calculadora_clt_pj
from apps.blog.sitemaps import StaticViewSitemap, BlogPostSitemap, ServicesSitemap, ImagesSitemap

# Customização do Admin
admin.site.site_header = "Vetorial - Administração"
admin.site.site_title = "Vetorial Admin"
admin.site.index_title = "Painel de Controle"


def health_check(request):
    """Endpoint de health check para monitoramento e load balancers."""
    from django.db import connection
    
    health = {
        'status': 'healthy',
        'database': 'ok',
        'cache': 'ok',
    }
    
    # Verifica conexão com banco de dados
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception as e:
        health['status'] = 'unhealthy'
        health['database'] = str(e)
    
    # Verifica conexão com cache (Redis)
    try:
        from django.core.cache import cache
        cache.set('health_check', 'ok', 1)
        if cache.get('health_check') != 'ok':
            raise Exception('Cache read/write failed')
    except Exception as e:
        health['cache'] = str(e)
        # Cache não é crítico, mantém healthy
    
    status_code = 200 if health['status'] == 'healthy' else 503
    return JsonResponse(health, status=status_code)

def home_view(request):
    from django.shortcuts import render
    from apps.support.models import Duvida
    from apps.dashboard.models import SocialMedia
    from apps.services.models import Plano
    
    testimonials = Testimonial.objects.filter(is_active=True)
    duvidas = Duvida.objects.filter(ativo=True)
    social_media = SocialMedia.objects.filter(is_active=True)
    
    # Buscar planos ativos separados por categoria
    planos_servicos = Plano.objects.filter(ativo=True, categoria='servicos').order_by('ordem', 'preco')
    planos_comercio = Plano.objects.filter(ativo=True, categoria='comercio').order_by('ordem', 'preco')
    
    return render(request, 'home.html', {
        'testimonials': testimonials,
        'duvidas': duvidas,
        'social_media': social_media,
        'planos_servicos': planos_servicos,
        'planos_comercio': planos_comercio,
    })

def abrir_empresa_view(request):
    from django.shortcuts import render
    from apps.services.models import Plano
    
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Buscar planos ativos separados por categoria
    planos_servicos = Plano.objects.filter(ativo=True, categoria='servicos').order_by('ordem', 'preco')
    planos_comercio = Plano.objects.filter(ativo=True, categoria='comercio').order_by('ordem', 'preco')
    
    return render(request, 'abrir_empresa.html', {
        'testimonials': testimonials,
        'planos_servicos': planos_servicos,
        'planos_comercio': planos_comercio,
    })

def deixar_mei_view(request):
    """Renderiza a página 'deixar_mei.html' separadamente para permitir edição independente."""
    from django.shortcuts import render
    from apps.services.models import Plano

    testimonials = Testimonial.objects.filter(is_active=True)

    # Buscar planos ativos separados por categoria
    planos_servicos = Plano.objects.filter(ativo=True, categoria='servicos').order_by('ordem', 'preco')
    planos_comercio = Plano.objects.filter(ativo=True, categoria='comercio').order_by('ordem', 'preco')

    return render(request, 'deixar_mei.html', {
        'testimonials': testimonials,
        'planos_servicos': planos_servicos,
        'planos_comercio': planos_comercio,
    })

def trocar_contador_view(request):
    """Renderiza a página 'trocar-contador.html' separadamente para permitir edição independente."""
    from django.shortcuts import render
    from apps.services.models import Plano

    testimonials = Testimonial.objects.filter(is_active=True)

    # Buscar planos ativos separados por categoria
    planos_servicos = Plano.objects.filter(ativo=True, categoria='servicos').order_by('ordem', 'preco')
    planos_comercio = Plano.objects.filter(ativo=True, categoria='comercio').order_by('ordem', 'preco')

    return render(request, 'trocar-contador.html', {
        'testimonials': testimonials,
        'planos_servicos': planos_servicos,
        'planos_comercio': planos_comercio,
    })

def contabilidade_completa_view(request):
    """Renderiza a página 'contabilidade-completa.html' separadamente para permitir edição independente."""
    from django.shortcuts import render
    from apps.services.models import Plano

    testimonials = Testimonial.objects.filter(is_active=True)

    # Buscar planos ativos separados por categoria
    planos_servicos = Plano.objects.filter(ativo=True, categoria='servicos').order_by('ordem', 'preco')
    planos_comercio = Plano.objects.filter(ativo=True, categoria='comercio').order_by('ordem', 'preco')

    return render(request, 'contabilidade-completa.html', {
        'testimonials': testimonials,
        'planos_servicos': planos_servicos,
        'planos_comercio': planos_comercio,
    })

def assessoria_view(request):
    """Renderiza a página 'assessoria.html' separadamente para permitir edição independente."""
    from django.shortcuts import render
    from apps.services.models import Plano

    testimonials = Testimonial.objects.filter(is_active=True)

    # Buscar planos ativos separados por categoria
    planos_servicos = Plano.objects.filter(ativo=True, categoria='servicos').order_by('ordem', 'preco')
    planos_comercio = Plano.objects.filter(ativo=True, categoria='comercio').order_by('ordem', 'preco')

    return render(request, 'assessoria.html', {
        'testimonials': testimonials,
        'planos_servicos': planos_servicos,
        'planos_comercio': planos_comercio,
    })
    

# Configuração dos Sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogPostSitemap,
    'services': ServicesSitemap,
    'images': ImagesSitemap,
}

urlpatterns = [
    path("health/", health_check, name='health_check'),
    path("", home_view, name='home'),
    path("abrir-empresa/", abrir_empresa_view, name='abrir_empresa'),
    path("deixar-mei/", deixar_mei_view, name='deixar_mei'),
    path("trocar-contador/", trocar_contador_view, name='trocar_contador'),
    path("contabilidade-completa/", contabilidade_completa_view, name='contabilidade_completa'),
    path("assessoria/", assessoria_view, name='assessoria'),
    
    # Novos Serviços
    path("contabilidade-mei/", TemplateView.as_view(template_name='services/contabilidade_mei.html'), name='contabilidade_mei'),
    path("endereco-virtual/", TemplateView.as_view(template_name='services/endereco_virtual.html'), name='endereco_virtual'),
    path("certificado-digital/", TemplateView.as_view(template_name='services/certificado_digital.html'), name='certificado_digital'),
    path("emissor-nota-fiscal/", TemplateView.as_view(template_name='services/emissor_nota_fiscal.html'), name='emissor_nota_fiscal'),
    path("contabilidade-online/", TemplateView.as_view(template_name='services/contabilidade_online.html'), name='contabilidade_online'),

    # Segmentos
    path("segmentos/servicos/", TemplateView.as_view(template_name='segments/servicos.html'), name='segmentos_servicos'),
    path("segmentos/comercio/", TemplateView.as_view(template_name='segments/comercio.html'), name='segmentos_comercio'),
    path("segmentos/saude/", TemplateView.as_view(template_name='segments/saude.html'), name='segmentos_saude'),
    path("segmentos/direito/", TemplateView.as_view(template_name='segments/direito.html'), name='segmentos_direito'),
    path("segmentos/engenharia/", TemplateView.as_view(template_name='segments/engenharia.html'), name='segmentos_engenharia'),
    path("segmentos/agronegocio/", TemplateView.as_view(template_name='segments/agronegocio.html'), name='segmentos_agronegocio'),
    path("segmentos/turismo/", TemplateView.as_view(template_name='segments/turismo.html'), name='segmentos_turismo'),
    path("segmentos/tecnologia/", TemplateView.as_view(template_name='segments/tecnologia.html'), name='segmentos_tecnologia'),
    path("segmentos/outros/", TemplateView.as_view(template_name='segments/outros.html'), name='segmentos_outros'),

    # Conteúdos
    path("conteudos/ebooks/", TemplateView.as_view(template_name='contents/ebooks.html'), name='conteudos_ebooks'),
    path("conteudos/educacao/", TemplateView.as_view(template_name='contents/educacao.html'), name='conteudos_educacao'),
    path("conteudos/regime-tributario/", TemplateView.as_view(template_name='contents/regime_tributario.html'), name='conteudos_regime_tributario'),

    path("obrigado/", TemplateView.as_view(template_name='obrigado.html'), name='obrigado'),
    # Páginas institucionais estáticas
    path('sobre/', TemplateView.as_view(template_name='pages/sobre.html'), name='sobre'),
    path('termos-de-uso/', TemplateView.as_view(template_name='pages/termos_de_uso.html'), name='termos_de_uso'),
    path('politica-de-privacidade/', TemplateView.as_view(template_name='pages/politica_de_privacidade.html'), name='politica_de_privacidade'),
    path("admin/", admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("dashboard/", include('apps.dashboard.urls')),
    path("users/", include('apps.users.urls')),
    path("services/", include('apps.services.urls')),
    path("blog/", include('apps.blog.urls')),
    path("documents/", include('apps.documents.urls')),
    path("payments/", include('apps.payments.urls')),
    path("recursos/calculadora-clt-pj/", calculadora_clt_pj, name='calculadora_clt_pj'),
    path("support/", include('apps.support.urls')),
    path("finance/", include('apps.finance.urls')),
    # path("payments/", include('apps.payments.urls')),
    
    # SEO - Sitemap e Robots
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
