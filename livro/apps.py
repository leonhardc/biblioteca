from django.apps import AppConfig


class LivroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'livro'

    def ready(self):
        import livro.signals.emprestimo
        import livro.signals.reserva
        import livro.signals.livro
        import livro.signals.autor
        import livro.signals.categoria
