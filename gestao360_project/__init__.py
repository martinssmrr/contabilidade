"""
Inicialização do projeto Gestão 360.
Importa a aplicação Celery para garantir que seja carregada quando o Django iniciar.
"""

# Importa a aplicação Celery
from .celery import app as celery_app

__all__ = ('celery_app',)
