from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Checkout
    path('checkout/<int:plano_id>/', views.checkout_plano, name='checkout_plano'),
    
    # API para processar pagamento
    path('api/processar/', views.processar_pagamento, name='processar_pagamento'),
    
    # Webhook do Mercado Pago
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
    
    # Páginas de resultado
    path('sucesso/', views.pagamento_sucesso, name='pagamento_sucesso'),
    path('erro/', views.pagamento_erro, name='pagamento_erro'),
    path('pendente/', views.pagamento_pendente, name='pagamento_pendente'),
]
