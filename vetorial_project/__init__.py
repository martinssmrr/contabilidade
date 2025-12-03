"""
Inicialização do projeto Vetorial com Celery.
"""

# Importar a aplicação Celery para que o Django a carregue automaticamente
from .celery import app as celery_app

__all__ = ('celery_app',)
