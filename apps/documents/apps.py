from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.documents"
    verbose_name = "Documentos"
    
    def ready(self):
        """
        Importa signals quando a aplicação estiver pronta.
        Garante que os signals sejam registrados no Django.
        """
        import apps.documents.signals  # noqa: F401
    verbose_name = "Documentos"
