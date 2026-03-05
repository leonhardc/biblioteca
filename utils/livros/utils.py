from livro.models import Reserva, Emprestimo, Livro
from usuario.models import Aluno, Professor, Funcionario
from utils.usuarios.utils import user_is_aluno, user_is_professor, user_is_funcionario
from usuario.constants import MAX_RESERVAS_POR_USUARIO
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from datetime import date

# Este modulo conta com uma serie de funcoes que serao uteis nas views do app livro

def reserva_existe(usuario, livro:Livro) -> bool:
    return Reserva.objects.filter(usuario=usuario, livro=livro, ativo=True).exists()

def emprestimo_existe(usuario, livro:Livro) -> bool:
    return Emprestimo.objects.filter(usuario=usuario, livro=livro, ativo=True).exists()

def retorna_pagina_anterior_com_erro(request:HttpRequest, mensagem_erro:str):
    messages.add_message(request, messages.ERROR, mensagem_erro)
    pagina_anterior = request.META.get('HTTP_REFERER')
    return redirect(pagina_anterior)

def cria_nova_reserva(request:HttpRequest, livro:Livro):
    Reserva.objects.create(
        usuario=request.user,
        livro=livro,
        data_reserva=date.today(), 
        ativo=True
    )
    messages.add_message(request, messages.SUCCESS, 'Reserva realizada com sucesso.')
    return redirect('livro:listar_reservas')

def criar_reserva_aluno(request:HttpRequest, id_livro:int):
    aluno = Aluno.objects.get(usuario=request.user)
    if aluno.reservas < MAX_RESERVAS_POR_USUARIO['aluno']:
        livro = Livro.objects.get(id=id_livro) # type: ignore
        if reserva_existe(request.user, livro):
            return retorna_pagina_anterior_com_erro(request, 'Reserva já existente para este livro.')
        if emprestimo_existe(request.user, livro):
            return retorna_pagina_anterior_com_erro(request, 'Empréstimo já existente para este livro.')
        # Se a reserva ou o emprestimo nao existir, cria uma nova reserva
        return cria_nova_reserva(request, livro)
    else:
        return retorna_pagina_anterior_com_erro(request, 'Nao eh possivel fazer mais reservas. Usuário já atingiu o numero máximo de reservas.')

def criar_reserva_professor(request:HttpRequest, id_livro:int):
    professor = Professor.objects.get(usuario=request.user)
    if professor.reservas < MAX_RESERVAS_POR_USUARIO['professor']:
        livro = Livro.objects.get(id=id_livro) # type: ignore
        if reserva_existe(request.user, livro):
            return retorna_pagina_anterior_com_erro(request, 'Reserva já existente para este livro.')
        if emprestimo_existe(request.user, livro):
            return retorna_pagina_anterior_com_erro(request, 'Empréstimo já existente para este livro.')
        # Se a reserva ou o emprestimo nao existir, cria uma nova reserva
        return cria_nova_reserva(request, livro)
    else:
        retorna_pagina_anterior_com_erro(request, 'Nao eh possivel fazer mais reservas. Usuário já atingiu o numero máximo de reservas.')

def criar_reserva_funcionario(request:HttpRequest, id_livro:int):
    funcionario = Funcionario.objects.get(usuario=request.user)
    if funcionario.reservas < MAX_RESERVAS_POR_USUARIO['funcionario']:
        livro = Livro.objects.get(id=id_livro) # type: ignore
        if reserva_existe(request.user, livro):
            return retorna_pagina_anterior_com_erro(request, 'Reserva já existente para este livro.')
        if emprestimo_existe(request.user, livro):
            return retorna_pagina_anterior_com_erro(request, 'Empréstimo já existente para este livro.')
        # Se a reserva ou o emprestimo nao existir, cria uma nova reserva
        return cria_nova_reserva(request, livro)
    else:
        return retorna_pagina_anterior_com_erro(request, 'Nao eh possivel fazer mais reservas. Usuário já atingiu o numero máximo de reservas.')
