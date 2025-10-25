from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from usuario.forms import LoginForm, FormularioAluno
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuario.models import Aluno, Professor, Funcionario
# from livro.models import Livro, Autor, Categoria, Reserva, Emprestimo
# from curso.models import Curso
# from django.core.paginator import Paginator
from utils.utils import *

# TODO: Essa view só pode ser acessada se o usuário estiver logado
def index(request:HttpRequest) -> HttpResponse:
    template = 'usuario/index.html'
    return render(
        request,
        template,
        context={
            'user':'Usuário'
        }
    )


def autentica_informacoes_de_usuario(request:HttpRequest):
    pass


def entrar(request:HttpRequest):
    template = 'usuario/entrar.html'
    if request.method == 'GET':
        formulario = LoginForm()
        return render(
            request, 
            template_name=template, 
            context={'form':formulario}
            )


def autenticar(request:HttpRequest):
    # Faz a autenticação de usuário
    if request.method == 'POST':
        formularioLogin = LoginForm(request.POST)
        if formularioLogin.is_valid():
            usuario = authenticate(
                username=formularioLogin.cleaned_data['usuario'],
                password=formularioLogin.cleaned_data['senha']
            )
            if usuario is None:
                messages.error(request, 'Usuário não autorizado.')
                return redirect('usuario:entrar')
            login(request, usuario)
            if user_is_aluno(usuario):
                # TODO: MUDAR PARA RETORNAR AS PAGINAS DE USUARIO
                # return HttpResponse('Pagina de Aluno')
                template_name='livro/livros.html'
                return render(request, template_name=template_name)
            elif user_is_professor(usuario):
                return HttpResponse('Pagina de Professor')
            elif user_is_funcionario(usuario):
                return HttpResponse('Pagina de Funcionario')
            else: 
                messages.info(request, 'Usuario ou senhas inválidos')
                return redirect('usuario:entrar')
        else:
            # Formulário inválido
            messages.info(request, 'Formulário inválido')
            return redirect('usuario:entrar')

# TODO: Essa view só pode ser acessada se o usuário estiver logado
def sair(request:HttpRequest):
    logout(request)
    return redirect('usuario:entrar')


# CRUD de Aluno
def listar_alunos(request:HttpRequest):
    query_alunos = Aluno.objects.all()
    return render(request, 'lista_alunos.html', context={'alunos':query_alunos})


def criar_aluno(request:HttpRequest):
    if request.method == 'GET':
        formulario_aluno = FormularioAluno()
        template_name = 'formulario-cadastro-aluno.html'
        return render(request, template_name, context={'form':formulario_aluno})
    else: 
        if request.method == 'POST':
            # TODO: Salvar as informações de usuário e aluno do formulário no banco de dados
            formulario_novo_aluno = FormularioAluno(request.POST)
            # TODO: Implementar página de retorno com mensagem de sucesso
            if formulario_novo_aluno.is_valid():
                return HttpResponse('OK')
            else:
                return render(request, template_name='formulario-cadastro-aluno.html', context={'form':formulario_novo_aluno})
    

def ler_aluno(request:HttpRequest, uid:int):
    pass

def atualizar_aluno(request:HttpRequest, uid:int):
    pass

def deletar_aluno(request:HttpRequest, uid:int):
    pass

# TODO: Mudar as views de detalhes para o app de administrador
def detalhes_aluno(request:HttpRequest, uid:int):
    if request.method == 'GET':
        template_name = 'admin/dashboard_admin_detalhes_usuarios.html'
        aluno = Aluno.objects.get(id=uid)
        contexto = {'aluno': aluno}
        return render(request, template_name, context=contexto)

# CRUD de Professor
def criar_professor(request:HttpRequest):
    pass

def ler_professor(request:HttpRequest, uid:int):
    pass

def atualizar_professor(request:HttpRequest, uid:int):
    pass

def deletar_professor(request:HttpRequest, uid:int):
    pass

def detalhes_professor(request:HttpRequest, uid:int):
    if request.method=='GET':
        template_name = 'admin/dashboard_admin_detalhes_usuarios.html'
        professor = Professor.objects.get(id=uid)
        contexto = {}
        contexto['professor'] = professor
        return render(request, template_name, context=contexto) # type: ignore


# CRUD de Funcionário
def criar_funcionario(request:HttpRequest):
    pass

def ler_funcionario(request:HttpRequest, uid:int):
    pass

def atualizar_funcionario(request:HttpRequest, uid:int):
    pass

def deletar_funcionario(request:HttpRequest, uid:int):
    pass

def detalhes_funcionario(request:HttpRequest, uid:int):
    if request.method=='GET':
        template_name = 'admin/dashboard_admin_detalhes_usuarios.html'
        funcionario = Funcionario.objects.get(id=uid)
        return render(request, template_name, context={'funcionario':funcionario})
