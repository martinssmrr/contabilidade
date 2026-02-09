from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Password Reset Flow
    path('esqueci-senha/', views.forgot_password_view, name='forgot_password'),
    path('verificar-codigo/', views.verify_code_view, name='verify_code'),
    path('redefinir-senha/', views.reset_password_view, name='reset_password'),

    path('area-cliente/', views.area_cliente, name='area_cliente'),
    path('notas-fiscais/', views.notas_fiscais, name='notas_fiscais'),
    path('notas-fiscais/emitir/', views.emitir_nfse, name='emitir_nfse'),
    path('notas-fiscais/tutorial/', views.tutorial_nfse, name='tutorial_nfse'),
    path('notas-fiscais/importar/', views.importar_notas, name='importar_notas'),
    path('notas-fiscais/consultar/', views.consultar_notas, name='consultar_notas'),
    path('notas-fiscais/cancelar/', views.cancelar_nota, name='cancelar_nota'),
    path('notas-fiscais/tomadas/', views.notas_tomadas, name='notas_tomadas'),
    path('notas-fiscais/aliquota/', views.minha_aliquota, name='minha_aliquota'),
    path('pendencias/', views.pendencias, name='pendencias'),
    path('pendencias/certidoes-negativas/', views.certidoes_negativas, name='certidoes_negativas'),
    path('pendencias/guias-pagamento/', views.guias_pagamento, name='guias_pagamento'),
    path('pendencias/historico-imposto/', views.historico_imposto, name='historico_imposto'),
    path('pendencias/simulador-imposto/', views.simulador_imposto, name='simulador_imposto'),
    path('financeiro/', views.financeiro, name='financeiro'),
    path('minha-empresa/', views.minha_empresa, name='minha_empresa'),
    path('mensalidade/', views.mensalidade, name='mensalidade'),
    path('mensalidade/ver-faturas/', views.ver_faturas, name='ver_faturas'),
    path('mensalidade/historico/', views.historico_pagamentos, name='historico_pagamentos'),
    path('mensalidade/formas-pagamento/', views.formas_pagamento, name='formas_pagamento'),
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
    path('servicos-avulsos/contratar/<int:servico_id>/', views.contratar_servico_avulso, name='contratar_servico_avulso'),
    path('servicos-avulsos/minhas-contratacoes/', views.minhas_contratacoes_avulsas, name='minhas_contratacoes_avulsas'),
    path('indique-ganhe/', views.indique_ganhe, name='indique_ganhe'),
    path('meu-perfil/', views.meu_perfil, name='meu_perfil'),
]
