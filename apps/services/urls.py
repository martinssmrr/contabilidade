from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'services'

urlpatterns = [
    path('', TemplateView.as_view(template_name='services.html'), name='services_list'),
    
    # Wizard de Abertura de Empresa
    path('abertura-empresa/', views.abertura_empresa_wizard, name='abertura_empresa'),
    path('abertura-empresa/<int:etapa>/', views.abertura_empresa_wizard, name='abertura_empresa'),
    
    # Pagamento
    path('abertura-empresa/<int:processo_id>/pagamento/', views.pagamento_abertura, name='pagamento_abertura'),
    path('abertura-empresa/<int:processo_id>/confirmar-pagamento/', views.confirmar_pagamento, name='confirmar_pagamento'),
    path('abertura-empresa/<int:processo_id>/sucesso/', views.processo_sucesso, name='processo_sucesso'),
    
    # API
    path('api/buscar-cep/', views.buscar_cep, name='buscar_cep'),
]
