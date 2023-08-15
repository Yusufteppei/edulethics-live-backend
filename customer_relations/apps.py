from django.apps import AppConfig


class CustomerRelationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_relations'

    def ready(self):
        import customer_relations.signals
