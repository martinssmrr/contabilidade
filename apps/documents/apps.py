from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class DocumentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.documents"
    verbose_name = "Documentos"
    
    def ready(self):
        """
        Importa signals quando a aplicação estiver pronta.
        Garante que os signals sejam registrados no Django.
        """
        # Importar signals
        import apps.documents.signals  # noqa: F401
        
        # Chamar função de registro explícito
        from apps.documents.signals import register_signals
        register_signals()
        
        print("✅ DocumentsConfig.ready() executado - Signals carregados!")
        logger.info("DocumentsConfig.ready() executado - Signals carregados!")
