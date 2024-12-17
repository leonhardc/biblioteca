from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuario.forms.formularios import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    return HttpResponse('Index')

def entrar(request):
    # Página de Login
    template = 'usuario/entrar.html'
    if request.method == 'GET':
        formulario = LoginForm()
        return render(request, template_name=template, context={'form':formulario})

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
            messages.info(request, f'{formularioLogin.changed_data['usuario']} logado com Sucesso')
            return redirect('index')

                
    return HttpResponse('Inicio')


def sair(request):
    # Faz logout no sistema e volta para página inicial'
    pass