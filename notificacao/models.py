from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationType(models.TextChoices):
    EMPRESTIMO_DEVOLVIDO = 'EMPRESTIMO_DEVOLVIDO', 'Empréstimo devolvido'
    RESERVA_CRIADA = 'RESERVA_CRIADA', 'Reserva criada'
    RESERVA_CANCELADA = 'RESERVA_CANCELADA', 'Reserva cancelada'
    EMPRESTIMO_ATRASADO = 'EMPRESTIMO_ATRASADO', 'Empréstimo atrasado'

class Notificacao(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    type = models.CharField(
        max_length=50,
        choices=NotificationType.choices
    )
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.type}] {self.title}'
