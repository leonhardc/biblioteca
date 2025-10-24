from datetime import datetime, timedelta

from django.http import HttpRequest
from django.shortcuts import redirect
from usuario.constants import NUM_MAX_EMPRESTIMOS, NUM_MAX_DIAS_EMPRESTIMOS
from usuario.models import Aluno, Professor, Funcionario
from django.contrib.auth.models import User
from usuario.forms import FormularioAluno, FormularioFuncionario, FormularioProfessor
from livro.forms import FormularioCriarEmprestimo
from livro.models import Emprestimo, Livro, Reserva
from django.contrib import messages
import random
# from django.db.models.query import QuerySet


def formatar_endereco(formulario:FormularioAluno|FormularioProfessor|FormularioFuncionario):
    tipo_logadouro = formulario.cleaned_data['tipo_logradouro'] # type: ignore
    logadouro = formulario.cleaned_data['logradouro']           # type: ignore
    numero = formulario.cleaned_data['numero']                  # type: ignore
    bairro = formulario.cleaned_data['bairro']                  # type: ignore
    cep = formulario.cleaned_data['cep']                        # type: ignore
    cidade = formulario.cleaned_data['cidade']                  # type: ignore
    estado = formulario.cleaned_data['estado']                  # type: ignore
    complemento = formulario.cleaned_data['complemento']        # type: ignore
    return f'{tipo_logadouro} {logadouro}, {numero}, {complemento} - {bairro}. CEP: {cep}. {cidade}/{estado}'

def gerar_matricula_aluno():
    while(True):
        matricula = f'{random.randint(100000, 999999)}'
        aluno = Aluno.objects.filter(matricula=matricula).exists()
        if not aluno:
            break
    return matricula

def gerar_matricula_professor():
    while(True):
        matricula = f'{random.randint(1000, 9999)}'
        professor = Professor.objects.filter(matricula=matricula).exists()
        if not professor:
            break
    return matricula

def gerar_matricula_funcionario():
    while(True):
        matricula = f'{random.randint(1000, 9999)}'
        funcionario = Funcionario.objects.filter(matricula=matricula).exists()
        if not funcionario:
            break
    return matricula

def gerar_data():
    data_inicio = datetime(1900, 1, 1)  
    data_fim = datetime(2025, 12, 31)   
    dias_aleatorios = random.randint(0, (data_fim - data_inicio).days)
    return data_inicio + timedelta(days=dias_aleatorios)

def separar_endereco(endereco:str):
    """
        Formato de endereço aceito:
        f'{tipo_logadouro} {logadouro}, {numero}, {complemento} - {bairro}. CEP: {cep}. {cidade}/{estado}'
    """
    try:
        logradouro, numero, outros = endereco.split(',')
        complemento_bairro, cep, cidade_estado = outros.split('.')
        complemento, bairro = complemento_bairro.split('-')
        cidade, estado = cidade_estado.split('/')

        tipo_logradouro = logradouro.split(' ')[0].strip()
        logradouro = ' '.join(logradouro.split(' ')[1:]).strip()
        numero = numero.strip()
        complemento = complemento.strip()
        bairro = bairro.strip()
        cep = ''.join([dig for dig in cep if dig.isdigit()])
        cidade = cidade.strip()
        estado = estado.strip()
        return {
            'tipo_logradouro':tipo_logradouro,
            'logradouro':logradouro, 
            'numero':numero, 
            'complemento':complemento, 
            'bairro':bairro,
            'cep':cep, 
            'cidade':cidade, 
            'estado':estado, 
            }
    except:
        return {
            'tipo_logradouro': '',
            'logradouro':'', 
            'numero':'', 
            'complemento':'', 
            'bairro':'',
            'cep':'', 
            'cidade':'', 
            'estado':'', 
        }


def retorna_instancia_usuario(usuario:User):
    if Aluno.objects.filter(usuario=usuario).exists():
        return Aluno.objects.get(usuario=usuario)
    elif Professor.objects.filter(usuario=usuario).exists():
        return Professor.objects.get(usuario=usuario)
    elif Funcionario.objects.filter(usuario=usuario).exists():
        return Funcionario.objects.get(usuario=usuario)
    else:
        return None


def salvar_emprestimo(request:HttpRequest, formulario:FormularioCriarEmprestimo, tipo_usuario:str):
    try:
        url_redirect = '/administrador/livros'
        usuario_obj = User.objects.get(id=formulario.cleaned_data['usuario'])
        num_emprestimos_por_usuario = Emprestimo.objects.filter(usuario=usuario_obj).count()
        if  num_emprestimos_por_usuario >= NUM_MAX_EMPRESTIMOS[tipo_usuario]:
            messages.add_message(
                request, 
                messages.INFO, 
                f"O usuário {usuario_obj.username} não pode alugar mais de {NUM_MAX_EMPRESTIMOS[tipo_usuario]} livros." # type: ignore
            ) 
            return redirect(url_redirect)
        livro_obj = Livro.objects.get(id=formulario.cleaned_data['livro'])
        if livro_obj.copias <= 0: # type: ignore
            messages.add_message(request, messages.ERROR, 'Esse livro não pode mais ser alugado.')
            return redirect(url_redirect)
        Emprestimo.objects.create(
            usuario = usuario_obj,
            livro = livro_obj,
            data_emprestimo = formulario.cleaned_data['data_emprestimo'],
            data_devolucao = formulario.cleaned_data["data_emprestimo"] + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS[tipo_usuario])
        )
        # Atualizar numero de cópias
        livro_obj.copias -= 1 # type: ignore
        livro_obj.save()
        messages.add_message(request, messages.SUCCESS, 'Emprestimo registrado com sucesso.')
        return redirect(url_redirect)
    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Um erro aconteceu ao tentar registrar o emprestimo.{e}')
        return redirect(url_redirect) # type: ignore


def pegar_informacoes_aluno(aluno:Aluno) -> dict[str, Aluno|Reserva|Emprestimo]:
    # TODO: Implementar essa função
    reservas = Reserva.objects.filter(usuario=aluno.usuario) # type: ignore
    emprestimos = Emprestimo.objects.filter(usuario=aluno.usuario) # type: ignore
    return {
        'aluno': aluno,
        'reservas': reservas,
        'emprestimos': emprestimos
    } # type: ignore


def pegar_informacoes_professor(professor:Professor) -> dict[str, Professor|Reserva|Emprestimo]: # type: ignore
    # TODO: Implementar essa função
    reservas = Reserva.objects.filter(usuario=professor.usuario) # type: ignore
    emprestimos = Emprestimo.objects.filter(usuario=professor.usuario) # type: ignore
    return {
        'professor': professor,
        'reservas': reservas,
        'emprestimos': emprestimos
    } # type: ignore
    pass


def pegar_informacoes_funcionario(funcionario:Funcionario) ->  dict[str, Funcionario|Reserva|Emprestimo]: # type: ignore
    # TODO: Implementar essa função
    reservas = Reserva.objects.filter(usuario=funcionario.usuario) # type: ignore
    emprestimos = Emprestimo.objects.filter(usuario=funcionario.usuario) # type: ignore
    return {
        'funcionario': funcionario,
        'reservas': reservas,
        'emprestimos': emprestimos
    } # type: ignore
    pass

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