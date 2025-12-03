"""
Configuração do Celery para o projeto Gestão 360.

Este módulo configura o Celery para processar tasks assíncronas.
"""
import os
from celery import Celery

# Define o settings module padrão
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao360_project.settings')

# Cria a aplicação Celery
app = Celery('gestao360_project')

# Carrega configurações do Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks de todos os apps instalados
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Task de debug para testar o Celery."""
    print(f'Request: {self.request!r}')
