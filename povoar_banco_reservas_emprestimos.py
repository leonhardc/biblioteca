from usuario.constants import NUM_MAX_EMPRESTIMOS, NUM_MAX_DIAS_EMPRESTIMOS
from livro.models import Livro, Emprestimo, Reserva
from usuario.models import Aluno, Professor, Funcionario
from datetime import datetime, timedelta
import random

def reservar_livro(usuario, livro):
    return Reserva.objects.create(
        usuario = usuario,
        livro = livro,
        data_reserva = datetime.now(),
        ativo = True
    )

def emprestar_livro(usuario, livro, tipo_usuario):
    return Emprestimo.objects.create(
        usuario = usuario,
        livro = livro,
        data_emprestimo = datetime.now(),
        data_devolucao = datetime.now() + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS[tipo_usuario]),
        pendente = False, 
        ativo = True, 
        numero_renovacoes = 0
    )

livros = Livro.objects.all()
# Reservas
def reservar_livro_aluno():
    alunos = Aluno.objects.all()
    for aluno in alunos:
        usuario = aluno.usuario
        livro = random.choice(livros)
        reservar_livro(usuario, livro)

def reservar_livro_professor():
    professores = Professor.objects.all()
    for professor in professores:
        usuario = professor.usuario
        livro = random.choice(livros)
        reservar_livro(usuario, livro)

def reservar_livro_funcionario():
    funcionarios = Funcionario.objects.all()
    for funcionario in funcionarios:
        usuario = funcionario.usuario
        livro = random.choice(livros)
        reservar_livro(usuario, livro)

# Emprestimos
def emprestar_livro_aluno():
    alunos = Aluno.objects.all()
    for aluno in alunos:
        emprestar_livro()

def emprestar_livro_professor():
    pass

def emprestar_livro_funcionario():
    pass
