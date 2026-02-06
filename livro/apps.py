from django.apps import AppConfig


class LivroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'livro'

    def ready(self):
        import livro.signals  # noqa
