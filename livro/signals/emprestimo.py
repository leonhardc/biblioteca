import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from livro.models import Emprestimo
from notificacao.models import Notificacao, NotificationType

logger = logging.getLogger('livro')

@receiver(post_save, sender=Emprestimo)
def emprestimo_criado(sender, instance, created, **kwargs):
    if not created:
        return

    logger.info(
        'Empréstimo criado | id=%s | livro_id=%s | usuario_id=%s | data_emprestimo=%s',
        instance.id,
        instance.livro_id,
        instance.usuario_id,
        instance.data_emprestimo
    )

    notificacao = Notificacao(
        user=instance.usuario,
        # type=NotificationType.EMPRESTIMO_CRIADO,
        title=f'Livro "{instance.livro.titulo}" emprestado',
        message=f'Você fez um empréstimo do livro "{instance.livro.titulo}".'
    )
    notificacao.save()

@receiver(post_save, sender=Emprestimo)
def emprestimo_devolvido(sender, instance, created, **kwargs):
    if not instance.pk:
        return
    
    antigo = Emprestimo.objects.get(pk=instance.pk)

    if antigo.ativo and not instance.ativo:
        logger.info(
            'Empréstimo devolvido | id=%s | livro_id=%s | usuario_id=%s | data_devolucao=%s',
            instance.id,
            instance.livro_id,
            instance.usuario_id,
            timezone.now()
        )

        notificacao = Notificacao(
            user=instance.usuario,
            # type=NotificationType.EMPRESTIMO_DEVOLVIDO,
            title=f'Livro "{instance.livro.titulo}" devolvido',
            message=f'Você devolveu o livro "{instance.livro.titulo}".'
        )
        notificacao.save()

@receiver(pre_save, sender=Emprestimo)
def emprestimo_pendente(sender, instance, **kwargs):
    if not instance.pk:
        return

    antigo = Emprestimo.objects.get(pk=instance.pk)

    if not antigo.pendente and instance.pendente:
        logger.warning(
            'Empréstimo pendente | id=%s | usuario=%s | livro="%s"',
            instance.id,
            instance.usuario,
            instance.livro
        )

        Notificacao.objects.create(
            user=instance.usuario,
            # type=NotificationType.EMPRESTIMO_ATRASADO,
            title='Empréstimo pendente ⚠️',
            message=(
                f'O empréstimo do livro "{instance.livro}" '
                f'foi marcado como pendente. Verifique sua situação.'
            )
        )

@receiver(pre_save, sender=Emprestimo)
def emprestimo_renovado(sender, instance, **kwargs):
    if not instance.pk:
        return

    antigo = Emprestimo.objects.get(pk=instance.pk)

    if instance.numero_renovacoes > antigo.numero_renovacoes:
        logger.info(
            'Empréstimo renovado | id=%s | usuario=%s | livro="%s" | renovacoes=%s',
            instance.id,
            instance.usuario,
            instance.livro,
            instance.numero_renovacoes
        )

        Notificacao.objects.create(
            user=instance.usuario,
            # type=NotificationType.EMPRESTIMO_RENOVADO,
            title='Empréstimo renovado 🔄',
            message=(
                f'O empréstimo do livro "{instance.livro}" '
                f'foi renovado. Total de renovações: '
                f'{instance.numero_renovacoes}.'
            )
        )

