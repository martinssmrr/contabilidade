from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('area-cliente/', views.area_cliente, name='area_cliente'),
    path('notas-fiscais/', views.notas_fiscais, name='notas_fiscais'),
    path('pendencias/', views.pendencias, name='pendencias'),
    path('certidoes-negativas/', views.pendencias, name='certidoes_negativas'),
    path('financeiro/', views.financeiro, name='financeiro'),
    path('minha-empresa/', views.minha_empresa, name='minha_empresa'),
    path('documentos/', views.documentos, name='documentos'),
    path('contabilidade/', views.contabilidade, name='contabilidade'),
    # API endpoints for dashboard
    path('api/contabilidade/summary/', views.api_contabilidade_summary, name='api_contabilidade_summary'),
    path('api/certidoes/status/', views.api_certidoes_status, name='api_certidoes_status'),
    # API endpoints for contabilidade (AJAX)
    path('contabilidade/add/', views.add_movimentacao, name='contabilidade_add'),
    path('contabilidade/edit/<int:pk>/', views.edit_movimentacao, name='contabilidade_edit'),
    path('contabilidade/delete/<int:pk>/', views.delete_movimentacao, name='contabilidade_delete'),
    path('contabilidade/transmit/', views.transmit_movimentacoes, name='contabilidade_transmit'),
    path('contabilidade/history/', views.contabilidade_history, name='contabilidade_history'),
    path('contabilidade/drafts/', views.drafts_by_month, name='contabilidade_drafts_by_month'),
    path('contabilidade/months/', views.months_transmitted, name='contabilidade_months'),
    path('contabilidade/month/<int:pk>/', views.transmitted_month_detail, name='contabilidade_month_detail'),
    path('meu-plano/', views.meu_plano, name='meu_plano'),
    path('servicos-avulsos/', views.servicos_avulsos, name='servicos_avulsos'),
    path('indique-ganhe/', views.indique_ganhe, name='indique_ganhe'),
]
