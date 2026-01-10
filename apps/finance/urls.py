from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transaction/add/', views.add_transaction, name='add_transaction'),
    path('subcategory/add/', views.add_subcategory, name='add_subcategory'),
    path('account/add/', views.add_account, name='add_account'),
    path('transmit/', views.transmit_transactions, name='transmit_transactions'),
    path('api/accounts/', views.get_accounts_ajax, name='get_accounts_ajax'),
    path('manage/', views.manage_accounts, name='manage_accounts'),
    path('subcategory/<int:pk>/delete/', views.delete_subcategory, name='delete_subcategory'),
    path('subcategory/<int:pk>/edit/', views.edit_subcategory, name='edit_subcategory'),
    path('account/<int:pk>/delete/', views.delete_account, name='delete_account'),
    path('account/<int:pk>/edit/', views.edit_account, name='edit_account'),
    path('subcategory/new/', views.new_subcategory, name='new_subcategory'),
    path('account/new/', views.new_account, name='new_account'),
    path('transaction/<int:pk>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transaction/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    path('report/pdf/', views.generate_report_pdf, name='generate_report_pdf'),
    path('scheduled/add/', views.add_scheduled_transaction, name='add_scheduled_transaction'),
    path('scheduled/list/', views.list_scheduled_transactions, name='list_scheduled_transactions'),
    path('scheduled/<int:pk>/liquidate/', views.liquidate_scheduled_transaction, name='liquidate_scheduled_transaction'),
    path('scheduled/<int:pk>/delete/', views.delete_scheduled_transaction, name='delete_scheduled_transaction'),
    path('reconciliation/', views.reconciliation_view, name='reconciliation'),
    path('reconciliation/<int:pk>/approve/', views.approve_reconciliation, name='approve_reconciliation'),
    path('reconciliation/<int:pk>/ignore/', views.ignore_reconciliation, name='ignore_reconciliation'),
]
