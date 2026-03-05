from usuario.models import Aluno, Professor, Funcionario


def user_is_aluno(usuario): # type: ignore
    if type(usuario) == int:
        aluno = Aluno.objects.filter(usuario=usuario).exists() 
        return True if aluno else False   
    else:
        username = usuario.username # type: ignore
        aluno = Aluno.objects.filter(usuario__username=username).exists()
        return True if aluno else False

def user_is_professor(usuario): # type: ignore
    if type(usuario) == int:
        professor = Professor.objects.filter(usuario=usuario).exists()
        return True if professor else False
    else:
        username = usuario.username # type: ignore
        professor = Professor.objects.filter(usuario__username=username).exists()
        return True if professor else False

def user_is_funcionario(usuario): # type: ignore
    if type(usuario) == int:
        funcionario = Funcionario.objects.filter(usuario=usuario).exists()
        return True if funcionario else False   
    else:
        username = usuario.username # type: ignore
        funcionario = Funcionario.objects.filter(usuario__username=username).exists()
        return True if funcionario else False