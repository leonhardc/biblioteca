from django.shortcuts import redirect, render
from .models import Notificacao
from utils.usuarios.utils import user_is_aluno, user_is_professor, user_is_funcionario

# Create your views here.
def mostrar_notificacoes(request, id_usuario):
    if request.user.is_authenticated:
        user_context = {
            'aluno': user_is_aluno(request.user),
            'professor': user_is_professor(request.user),
            'funcionario': user_is_funcionario(request.user)
        }
        notificacoes = Notificacao.objects.filter(user_id=id_usuario)
        return render(request, 'usuario/notificacoes.html', {'notificacoes': notificacoes, 'user_context': user_context})
    
def detalhe_notificacao(request, id_notificacao):
    if request.user.is_authenticated:
        user_context = {
            'aluno': user_is_aluno(request.user),
            'professor': user_is_professor(request.user),
            'funcionario': user_is_funcionario(request.user)
        }
        notificacao = Notificacao.objects.get(id=id_notificacao)
        notificacao.is_read = True
        notificacao.save()
        return render(request, 'usuario/detalhe_notificacao.html', {'notificacao': notificacao, 'user_context': user_context})
    
def deletar_notificacao(request, id_notificacao):
    if request.user.is_authenticated:
        notificacao = Notificacao.objects.get(id=id_notificacao)
        notificacao.delete()
        return redirect('notificacao:notificacoes', id_usuario=request.user.id)