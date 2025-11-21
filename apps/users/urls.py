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
    path('financeiro/', views.financeiro, name='financeiro'),
    path('minha-empresa/', views.minha_empresa, name='minha_empresa'),
    path('documentos/', views.documentos, name='documentos'),
    path('contabilidade/', views.contabilidade, name='contabilidade'),
    path('meu-plano/', views.meu_plano, name='meu_plano'),
    path('servicos-avulsos/', views.servicos_avulsos, name='servicos_avulsos'),
    path('indique-ganhe/', views.indique_ganhe, name='indique_ganhe'),
]
