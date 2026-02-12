import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from livro.models import Categoria
from notificacao.models import Notificacao, NotificationType

logger = logging.getLogger('livro')

@receiver(post_save, sender=Categoria)
def categoria_criada(sender, instance, created, **kwargs):
    if not created:
        return

    logger.info(
        'Categoria criada | id=%s | categoria="%s"',
        instance.id,
        instance.categoria
    )

@receiver(post_save, sender=Categoria)
def categoria_atualizada(sender, instance, created, **kwargs):
    if created:
        return

    logger.info(
        'Categoria atualizada | id=%s | categoria="%s"',
        instance.id,
        instance.categoria
    )

@receiver(pre_save, sender=Categoria)
def categoria_excluida(sender, instance, **kwargs):
    if not instance.pk:
        return

    antigo = Categoria.objects.get(pk=instance.pk)

    if antigo.ativo and not instance.ativo:
        logger.info(
            'Categoria excluída | id=%s | categoria="%s"',
            instance.id,
            instance.categoria
        )