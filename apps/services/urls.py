from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'services'

urlpatterns = [
    path('', TemplateView.as_view(template_name='services.html'), name='services_list'),
    
    # Serviços
    path('abrir-mei/', views.abrir_mei_view, name='abrir_mei'),
    path('abrir-mei/solicitar/', views.solicitar_abertura_mei_view, name='solicitar_abertura_mei'),
    path('abrir-mei/checkout/<int:solicitacao_id>/', views.checkout_mei_view, name='checkout_mei'),
    path('abrir-mei/processar-pagamento/<int:solicitacao_id>/', views.processar_pagamento_mei, name='processar_pagamento_mei'),
    path('abrir-mei/sucesso/<int:solicitacao_id>/', views.mei_sucesso_view, name='mei_sucesso'),
    
    path('contabilidade-online/', TemplateView.as_view(template_name='services/contabilidade_online.html'), name='contabilidade_online'),
    
    # Planos
    path('planos/', views.planos_view, name='planos'),
    
    # Wizard de Abertura de Empresa
    path('abertura-empresa/', views.abertura_empresa_wizard, name='abertura_empresa'),
    path('abertura-empresa/<int:etapa>/', views.abertura_empresa_wizard, name='abertura_empresa'),
    
    # Pagamento
    path('abertura-empresa/<int:processo_id>/pagamento/', views.pagamento_abertura, name='pagamento_abertura'),
    path('abertura-empresa/<int:processo_id>/confirmar-pagamento/', views.confirmar_pagamento, name='confirmar_pagamento'),
    path('abertura-empresa/<int:processo_id>/sucesso/', views.processo_sucesso, name='processo_sucesso'),
    
    # Teste de Contrato
    path('contrato-teste/', views.contrato_test_view, name='contrato_test'),

    path('abertura-empresa/<int:processo_id>/contrato/', views.download_contrato, name='download_contrato'),
    
    # Recursos
    path('recursos/consultar-cnaes/', views.consulta_cnaes_view, name='consulta_cnaes'),
    
    # API
    path('api/buscar-cep/', views.buscar_cep, name='buscar_cep'),
]
