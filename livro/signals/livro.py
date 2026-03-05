from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from livro.models import Livro
import logging

logger = logging.getLogger('livro')


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import logging

from livro.models import Livro

logger = logging.getLogger('livro')


@receiver(post_save, sender=Livro)
def livro_criado(sender, instance, created, **kwargs):
    if not created:
        return

    logger.info(
        'Livro criado | id=%s | titulo="%s" | isbn=%s',
        instance.id,
        instance.titulo,
        instance.isbn
    )


@receiver(post_save, sender=Livro)
def livro_atualizado(sender, instance, created, **kwargs):
    if created:
        return

    logger.info(
        'Livro atualizado | id=%s | titulo="%s"',
        instance.id,
        instance.titulo
    )


@receiver(pre_save, sender=Livro)
def livro_sem_copias(sender, instance, **kwargs):
    if not instance.pk:
        return

    antigo = Livro.objects.get(pk=instance.pk)

    if antigo.copias > 0 and instance.copias == 0:
        logger.warning(
            'Livro sem cópias | id=%s | titulo="%s"',
            instance.id,
            instance.titulo
        )


@receiver(pre_save, sender=Livro)
def livro_com_copias(sender, instance, **kwargs):
    if not instance.pk:
        return

    antigo = Livro.objects.get(pk=instance.pk)

    if antigo.copias == 0 and instance.copias > 0:
        logger.info(
            'Livro voltou ao estoque | id=%s | titulo="%s" | copias=%s',
            instance.id,
            instance.titulo,
            instance.copias
        )

