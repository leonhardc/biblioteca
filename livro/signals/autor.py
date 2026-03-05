import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from livro.models import Autor
from notificacao.models import Notificacao, NotificationType

logger = logging.getLogger('livro')

@receiver(post_save, sender=Autor)
def autor_criado(sender, instance, created, **kwargs):
    if not created:
        return

    logger.info(
        'Autor criado | id=%s | nome="%s"',
        instance.id,
        instance.nome
    )

@receiver(post_save, sender=Autor)
def autor_atualizado(sender, instance, created, **kwargs):
    if created:
        return

    logger.info(
        'Autor atualizado | id=%s | nome="%s"',
        instance.id,
        instance.nome
    )

@receiver(pre_save, sender=Autor)
def autor_excluido(sender, instance, **kwargs):
    if not instance.pk:
        return

    antigo = Autor.objects.get(pk=instance.pk)

    if antigo.ativo and not instance.ativo:
        logger.info(
            'Autor excluído | id=%s | nome="%s"',
            instance.id,
            instance.nome
        )