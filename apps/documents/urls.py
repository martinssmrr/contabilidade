from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    # URLs do painel da equipe (staff)
    path('staff/clients/', views.client_list_view, name='client_list'),
    path('staff/clients/<int:pk>/', views.client_detail_view, name='client_detail'),
]
