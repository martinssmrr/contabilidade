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
from apps.services import views as service_views  # Added import
from apps.support.models import Duvida
from apps.services.models import Plano

# Customização do Admin
admin.site.site_header = "Vetorial - Administração"
admin.site.site_title = "Vetorial Admin"
admin.site.index_title = "Painel de Controle"

def home_view(request):
    from django.shortcuts import render
    from apps.support.models import Duvida
    from apps.services.models import Plano
    
    testimonials = Testimonial.objects.filter(is_active=True)
    duvidas = Duvida.objects.filter(ativo=True)
    
    # Buscar planos ativos separados por categoria
    planos_servicos = Plano.objects.filter(ativo=True, categoria='servicos').order_by('ordem', 'preco')
    planos_comercio = Plano.objects.filter(ativo=True, categoria='comercio').order_by('ordem', 'preco')
    
    return render(request, 'home.html', {
        'testimonials': testimonials,
        'duvidas': duvidas,
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

def depoimentos_view(request):
    from django.shortcuts import render
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, 'pages/depoimentos.html', {
        'testimonials': testimonials,
    })

def faq_view(request):
    from django.shortcuts import render
    duvidas = Duvida.objects.filter(ativo=True).order_by('ordem', '-criado_em')
    return render(request, 'pages/faq.html', {
        'duvidas': duvidas,
    })

def quanto_custa_view(request):
    from django.shortcuts import render
    planos_servicos = Plano.objects.filter(ativo=True, categoria='servicos').order_by('ordem', 'preco')
    planos_comercio = Plano.objects.filter(ativo=True, categoria='comercio').order_by('ordem', 'preco')
    return render(request, 'pages/quanto_custa.html', {
        'planos_servicos': planos_servicos,
        'planos_comercio': planos_comercio,
    })

def contato_view(request):
    from django.shortcuts import render
    return render(request, 'pages/contato.html')

urlpatterns = [
    path("", home_view, name='home'),
    path("abrir-empresa/", abrir_empresa_view, name='abrir_empresa'),
    # Páginas institucionais estáticas
    path('sobre', TemplateView.as_view(template_name='pages/sobre.html'), name='sobre'),
    path('termos-de-uso', TemplateView.as_view(template_name='pages/termos_de_uso.html'), name='termos_de_uso'),
    path('politica-de-privacidade', TemplateView.as_view(template_name='pages/politica_de_privacidade.html'), name='politica_de_privacidade'),
    path('obrigado/', TemplateView.as_view(template_name='obrigado.html'), name='obrigado'),
    
    # Páginas institucionais novas
    path('depoimentos/', depoimentos_view, name='depoimentos'),
    path('trabalhe-conosco/', TemplateView.as_view(template_name='pages/trabalhe_conosco.html'), name='trabalhe_conosco'),
    path('gestao-contabil/', TemplateView.as_view(template_name='pages/gestao_contabil.html'), name='gestao_contabil'),
    path('bpo-financeiro/', TemplateView.as_view(template_name='pages/bpo_financeiro.html'), name='bpo_financeiro'),
    path('regularizacao-empresarial/', TemplateView.as_view(template_name='pages/regularizacao_empresarial.html'), name='regularizacao_empresarial'),
    path('contato/', contato_view, name='contato'),
    path('quanto-custa/', quanto_custa_view, name='quanto_custa'),
    path('faq/', faq_view, name='faq'),
    
    path("admin/", admin.site.urls),
    path("dashboard/", include('apps.dashboard.urls')),
    # Adicionar mais URLs conforme necessário:
    # path("accounts/", include('django.contrib.auth.urls')),  # Login/Logout padrão
    path("services/", include('apps.services.urls')),

    # URLs Raiz para páginas de serviços (Solicitadas pelo usuário)
    path("contabilidade-mei/", service_views.contabilidade_mei_view_debug, name='contabilidade_mei_lp'),
    path("contabilidade-mei/contratarplano", service_views.contratar_plano_mei_view, name='contratar_plano_mei'),

    # Alias para Abrir MEI na raiz
    path("abrir-mei/", service_views.abrir_mei_view, name='abrir_mei_root'),
    path("abrir-mei/contratarplano", service_views.contratar_plano_mei_view, name='contratar_plano_abrir_mei'),

    path("blog/", include('apps.blog.urls')),
    path("users/", include('apps.users.urls')),
    path("documents/", include('apps.documents.urls')),
    path("payments/", include('apps.payments.urls')),
    # path("support/", include('apps.support.urls')),
]

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
