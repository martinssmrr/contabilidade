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
from apps.testimonials.models import Testimonial
from apps.services.views import calculadora_clt_pj

# Customização do Admin
admin.site.site_header = "Vetorial - Administração"
admin.site.site_title = "Vetorial Admin"
admin.site.index_title = "Painel de Controle"

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

urlpatterns = [
    path("", home_view, name='home'),
    path("abrir-empresa/", abrir_empresa_view, name='abrir_empresa'),
    path("admin/", admin.site.urls),
    path("dashboard/", include('apps.dashboard.urls')),
    path("users/", include('apps.users.urls')),
    path("services/", include('apps.services.urls')),
    path("blog/", include('apps.blog.urls')),
    path("documents/", include('apps.documents.urls')),
    path("recursos/calculadora-clt-pj/", calculadora_clt_pj, name='calculadora_clt_pj'),
    path("support/", include('apps.support.urls')),
    # path("payments/", include('apps.payments.urls')),
]

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
