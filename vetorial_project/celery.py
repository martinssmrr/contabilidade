"""
Configuração do Celery para tarefas assíncronas.

Este módulo configura o Celery para processar tarefas em background,
incluindo envio de e-mails e outras operações que não devem bloquear
a resposta HTTP.

Autor: Sistema Vetorial
Data: 2025-12-02
"""

import os
from celery import Celery
from django.conf import settings

# Define o módulo de settings padrão para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')

# Cria a aplicação Celery
app = Celery('vetorial_project')

# Configuração usando namespace 'CELERY'
# Todas as configurações do Celery devem começar com CELERY_ no settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrir tasks automaticamente em todos os apps registrados
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Task de debug para testar se o Celery está funcionando."""
    print(f'Request: {self.request!r}')
