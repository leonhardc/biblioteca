import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from livro.models import Reserva
from notificacao.models import Notificacao, NotificationType

logger = logging.getLogger('livro')

@receiver(post_save, sender=Reserva)
def reserva_criada(sender, instance, created, **kwargs):
    if not created:
        return

    logger.info(
        'Reserva criada | id=%s | livro_id=%s | usuario_id=%s | data_reserva=%s',
        instance.id,
        instance.livro_id,
        instance.usuario_id,
        instance.data_reserva
    )

    notificacao = Notificacao(
        user=instance.usuario,
        type=NotificationType.RESERVA_CRIADA,
        title=f'Livro "{instance.livro.titulo}" reservado',
        message=f'Você fez uma reserva do livro "{instance.livro.titulo}".'
    )
    notificacao.save()

@receiver(pre_save, sender=Reserva)
def reserva_cancelada(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    antigo = Reserva.objects.get(pk=instance.pk)

    if antigo.ativo and not instance.ativo:
        logger.info(
            'Reserva cancelada | id=%s | livro_id=%s | usuario_id=%s | data_cancelamento=%s',
            instance.id,
            instance.livro_id,
            instance.usuario_id,
            instance.data_cancelamento
        )

        notificacao = Notificacao(
            user=instance.usuario,
            type=NotificationType.RESERVA_CANCELADA,
            title=f'Livro "{instance.livro.titulo}" reserva cancelada',
            message=f'Você cancelou a reserva do livro "{instance.livro.titulo}".'
        )
        notificacao.save()