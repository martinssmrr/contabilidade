from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('capturar-lead/', views.capturar_lead, name='capturar_lead'),
    
    # API Endpoints - Leads
    path('api/leads/', views.api_leads_list, name='api_leads_list'),
    path('api/leads/create/', views.api_leads_create, name='api_leads_create'),
    path('api/leads/<int:pk>/update/', views.api_leads_update, name='api_leads_update'),
    path('api/leads/<int:pk>/delete/', views.api_leads_delete, name='api_leads_delete'),
    path('api/leads/<int:pk>/send-whatsapp/', views.api_leads_send_whatsapp, name='api_leads_send_whatsapp'),
    
    # API Endpoints - Tickets
    path('api/tickets/', views.api_tickets_list, name='api_tickets_list'),
    
    # API Endpoints - Blog
    path('api/posts/', views.api_posts_list, name='api_posts_list'),
    path('api/categories/', views.api_categories_list, name='api_categories_list'),
    
    # API Endpoints - Testimonials
    path('api/testimonials/', views.api_testimonials_list, name='api_testimonials_list'),
    path('api/testimonials/<int:pk>/delete/', views.api_testimonials_delete, name='api_testimonials_delete'),
    
    # API Endpoints - Planos
    path('api/planos/', views.api_planos_list, name='api_planos_list'),
    path('api/planos/<int:pk>/delete/', views.api_planos_delete, name='api_planos_delete'),
    
    # API Endpoints - Documents
    path('api/documents/', views.api_documents_list, name='api_documents_list'),
    
    # API Endpoints - Chamados (Staff)
    path('api/chamados/', views.api_chamados_list, name='api_chamados_list'),
    path('api/chamados/<int:pk>/', views.api_chamado_detail, name='api_chamado_detail'),
    path('api/chamados/<int:pk>/respond/', views.api_chamado_respond, name='api_chamado_respond'),
    path('api/chamados/<int:pk>/update-status/', views.api_chamado_update_status, name='api_chamado_update_status'),
    
    # API Endpoints - Notas Fiscais (Staff)
    path('api/clientes/', views.api_clientes_list, name='api_clientes_list'),
    path('api/notas-fiscais/enviar/', views.api_nota_fiscal_enviar, name='api_nota_fiscal_enviar'),
    
    # Área do Cliente
    path('cliente/dashboard/', views.dashboard_cliente, name='dashboard_cliente'),
    path('cliente/abrir-chamado/', views.abrir_chamado, name='abrir_chamado'),
    path('cliente/chamado/<int:pk>/', views.chamado_detail, name='chamado_detail'),
    path('cliente/chamado/<int:pk>/responder/', views.responder_chamado, name='responder_chamado'),
]
