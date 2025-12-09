from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Pré-checkout (cadastro antes do pagamento)
    path('contratar/<int:plano_id>/', views.pre_checkout, name='pre_checkout'),
    
    # Checkout
    path('checkout/<int:plano_id>/', views.checkout_plano, name='checkout_plano'),
    
    # API para processar pagamento
    path('api/processar/', views.processar_pagamento, name='processar_pagamento'),
    
    # API para verificar status (polling)
    path('api/status/', views.verificar_status_pagamento, name='verificar_status'),
    
    # Webhook do Mercado Pago
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
    
    # Páginas de resultado
    path('sucesso/', views.pagamento_sucesso, name='pagamento_sucesso'),
    path('erro/', views.pagamento_erro, name='pagamento_erro'),
    path('pendente/', views.pagamento_pendente, name='pagamento_pendente'),
    path('pix/', views.pagamento_pix, name='pagamento_pix'),
    path('boleto/', views.pagamento_boleto, name='pagamento_boleto'),
]
