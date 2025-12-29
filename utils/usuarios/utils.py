from usuario.models import Aluno, Professor, Funcionario


def user_is_aluno(usuario): # type: ignore
    username = usuario.username # type: ignore
    aluno = Aluno.objects.filter(usuario__username=username).exists()
    return True if aluno else False

def user_is_professor(usuario): # type: ignore
    username = usuario.username # type: ignore
    professor = Professor.objects.filter(usuario__username=username).exists()
    return True if professor else False

def user_is_funcionario(usuario): # type: ignore
    username = usuario.username # type: ignore
    funcionario = Funcionario.objects.filter(usuario__username=username).exists()
    return True if funcionario else False