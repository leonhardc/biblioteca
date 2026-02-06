# Signals do app livro
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from livro.models import Emprestimo
from notificacao.models import Notificacao

@receiver(pre_save, sender=Emprestimo)
def emprestimo_devolvido(sender, instance, **kwargs):
    # 1. Se o objeto ainda nao existe no banco, sera criado
    if not instance.pk:
        return
    
    # 2. Busca o estado antigo
    antigo = Emprestimo.objects.get(pk=instance.pk)

    # 3. Detecta transicao false -> true no campo devolvido
    if antigo.ativo and not instance.ativo:
        instance.data_devolucao = timezone.now()
        Notificacao.objects.create(
            user=instance.usuario,
            title='Livro devolvido 📚',
            message=(
                f'O livro "{instance.livro}" '
                f'foi devolvido com sucesso.'
            )
        )