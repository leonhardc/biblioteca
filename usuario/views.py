from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuario.forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuario.forms import FormularioAluno

# TODO: Essa view só pode ser acessada se o usuário estiver logado
def index(request):
    template = 'usuario/index.html'
    return render(
        request,
        template,
        context={
            'user':'Usuário'
        }
    )


def entrar(request):
    # Carrega página de Login
    template = 'usuario/entrar.html'
    if request.method == 'GET':
        formulario = LoginForm()
        return render(
            request, 
            template_name=template, 
            context={'form':formulario}
            )


def autenticar(request):
    # Faz a autenticação de usuário
    if request.method == 'POST':
        formularioLogin = LoginForm(request.POST)
        if formularioLogin.is_valid():
            usuario = authenticate(
                username=formularioLogin.cleaned_data['usuario'],
                password=formularioLogin.cleaned_data['senha']
            )
            if usuario is None:
                # retorna para página de login com um código de erro
                messages.error(request, 'Usuário não autorizado.')
                return redirect('usuario:entrar')
            # Faz login e retorna a página inicial da aplicação
            # Mostra mensagem de sucesso no login
            login(request, usuario)
            messages.info(request, f'{formularioLogin.cleaned_data["usuario"]} logado com Sucesso')
            return redirect('usuario:index')
        else:
            # Formulário inválido
            messages.info(request, 'Formulário inválido')
            return redirect('usuario:entrar')

# TODO: Essa view só pode ser acessada se o usuário estiver logado
def sair(request):
    logout(request)
    return redirect('usuario:entrar')


# CRUD de Aluno
def criar_aluno(request):
    if request.method == 'GET':
        # TODO: Carregar formulário de inserção de dados para Aluno
        formulario_aluno = FormularioAluno()
        return render(request, template_name='form.html', context={'form':formulario_aluno})
        pass
    else: 
        if request.methof == 'POST':
            # TODO: Salvar as informações de usuário e aluno do formulário no banco de dados
            pass
    

def ler_aluno(request, uid):
    pass

def atualizar_aluno(request, uid):
    pass

def deletar_aluno(request, uid):
    pass


# CRUD de Professor
def criar_professor(request):
    pass

def ler_professor(request, uid):
    pass

def atualizar_professor(request, uid):
    pass

def deletar_professor(request, uid):
    pass


# CRUD de Funcionário
def criar_funcionario(request):
    pass

def ler_funcionario(request, uid):
    pass

def atualizar_funcionario(request, uid):
    pass

def deletar_funcionario(request, uid):
    pass
