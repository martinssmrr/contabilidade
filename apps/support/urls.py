from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('api/dashboard/stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
    path('api/processos-abertura/', views.api_processos_abertura_list, name='api_processos_abertura_list'),
    path('api/processos-abertura/<int:pk>/', views.api_processos_abertura_detail, name='api_processos_abertura_detail'),
    path('capturar-lead/', views.capturar_lead, name='capturar_lead'),
    
    # API Endpoints - Leads
    path('api/leads/', views.api_leads_list, name='api_leads_list'),
    # path('api/processos-abertura/', views.api_processos_abertura_list, name='api_processos_abertura_list'), # Moved up
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
    path('api/notas-fiscais/', views.api_notas_fiscais_list, name='api_notas_fiscais_list'),
    path('api/notas-fiscais/enviar/', views.api_nota_fiscal_enviar, name='api_nota_fiscal_enviar'),
    
    # API Endpoints - Contabilidade (Staff)
    path('api/contabilidade/clientes/', views.api_contabilidade_clientes, name='api_contabilidade_clientes'),
    path('api/contabilidade/clientes/<int:cliente_id>/movimentacoes/', views.api_contabilidade_movimentacoes, name='api_contabilidade_movimentacoes'),
    
    # API Endpoints - Certidões Negativas (Staff)
    path('api/certidoes/', views.api_certidoes_list, name='api_certidoes_list'),
    path('api/certidoes/enviar/', views.api_certidao_enviar, name='api_certidao_enviar'),
    
    # API Endpoints - Documentos da Empresa (Staff)
    path('api/documentos-empresa/', views.api_documentos_empresa_list, name='api_documentos_empresa_list'),
    path('api/documentos-empresa/enviar/', views.api_documento_empresa_enviar, name='api_documento_empresa_enviar'),
    path('api/clientes-fase/', views.api_clientes_fase_list, name='api_clientes_fase_list'),
    path('api/clientes-fase/update/', views.api_cliente_fase_update, name='api_cliente_fase_update'),
    
    # API Endpoints - Extratos Bancários (Staff)
    path('api/extratos-bancarios/clientes/', views.api_clientes_com_extratos, name='api_clientes_com_extratos'),
    path('api/extratos-bancarios/clientes/<int:cliente_id>/', views.api_extratos_bancarios_cliente, name='api_extratos_bancarios_cliente'),
    
    # Área do Cliente
    path('cliente/dashboard/', views.dashboard_cliente, name='dashboard_cliente'),
    path('cliente/abrir-chamado/', views.abrir_chamado, name='abrir_chamado'),
    path('cliente/chamado/<int:pk>/', views.chamado_detail, name='chamado_detail'),
    path('cliente/chamado/<int:pk>/responder/', views.responder_chamado, name='responder_chamado'),
    
    # API Endpoints - Novos (Extensão do Dashboard)
    path('api/guias/', views.api_guias_imposto_list, name='api_guias_imposto_list'),
    path('api/guias/enviar/', views.api_guia_imposto_enviar, name='api_guia_imposto_enviar'),
    path('api/cliente-assinatura/<int:cliente_id>/', views.api_cliente_subscription_info, name='api_cliente_subscription_info'),
    path('api/cliente-assinatura/update/', views.api_cliente_subscription_update, name='api_cliente_subscription_update'),

    # API Endpoints - Staff Tasks
    path('api/staff-tasks/', views.api_staff_tasks_list, name='api_staff_tasks_list'),
    path('api/staff-tasks/<int:pk>/update/', views.api_staff_tasks_update, name='api_staff_tasks_update'),
    path('api/staff-tasks/<int:pk>/delete/', views.api_staff_tasks_delete, name='api_staff_tasks_delete'),

    # API Endpoints - Agenda
    path('api/agenda/', views.api_agenda_list, name='api_agenda_list'),
    path('api/agenda/sync/', views.api_agenda_sync_google, name='api_agenda_sync_google'),
    path('api/agenda/create/', views.api_agenda_create, name='api_agenda_create'),
    path('api/agenda/<int:pk>/update/', views.api_agenda_update, name='api_agenda_update'),
    path('api/agenda/<int:pk>/update-status/', views.api_agenda_update_status, name='api_agenda_update_status'),
    path('api/agenda/<int:pk>/delete/', views.api_agenda_delete, name='api_agenda_delete'),
]
