# O que deve ser implementado aqui:
# TODO: 1. Todas as views de Usuarios. Elas tem que ser Intermediarias a todos as operações
# Que envolvam usuarios. 
# TODO: 2. Tem que ser Implementado o Sistema de Login Redirecionando cada um dos tipos de usuarios
# as suas respectivas paginas iniciais
# TODO: 3. Tem que ser implementado todo um sistema de controle de acesso a determinadas views. Onde cada
# tipo de usuario so pode acessar as views as quais ele tem permissao
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
from utils.formularios.utils_forms import informacoes_formulario_aluno
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
                template_name='usuario/aluno/dashboard_aluno.html'
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
    template_name = 'usuario/aluno/listar_alunos.html'
    return render(
        request, 
        template_name, 
        context={
            'alunos':Aluno.objects.all()
            }
        )

def dashaboard_aluno(request:HttpRequest):
    if request.method == "GET":
        template_name = "usuario/aluno/dashboard_aluno.html"
        contexto = {
            'dashboard': True,
        }
        return render(request, template_name, context=contexto)

def criar_aluno(request:HttpRequest):
    if request.method == 'GET':
        formulario_aluno = FormularioAluno()
        template_name = 'formulario-cadastro-aluno.html'
        return render(request, template_name, context={'form':formulario_aluno})
    if request.method == 'POST':
            pass

def ler_aluno(request:HttpRequest, uid:int):
    # TODO: O usuario do tipo aluno e usuario do tipo funcionario e administrador tem acesso a essa view
    # TODO: Criar o template abaixo
    template_name = "usuario/aluno/ler_aluno.html"
    if Aluno.objects.filter(id=uid).exists():
        aluno = Aluno.objects.get(id=uid)
        return render(request, template_name, context={'aluno':aluno})
    else: 
        url_anterior = request.META.get('HTTP_REFERER')
        messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
        return redirect(url_anterior)

def atualizar_aluno(request:HttpRequest, uid:int):
    # TODO: Essa view so pode ser acessada por funcionarios, administradores e pelo aluno
    # TODO: Criar o template abaixo
    template_name = 'usuario/aluno/atualizar_dados_aluno.html'
    if request.method == "GET":
        if Aluno.objects.filter(id=uid).exists():
            aluno = Aluno.objects.get(id=uid)
            endereco = separar_endereco(aluno.endereco) 
            data_aluno = informacoes_formulario_aluno(aluno, endereco)
            formulario = FormularioAluno(initial=data_aluno)
            return render(request, template_name, context={'aluno':aluno, 'form':formulario})
        else:
            messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior)
    if request.method == "POST":
        # TODO: Salvar os dados do aluno no banco de dados
        pass

def deletar_aluno(request:HttpRequest, uid:int):
    # TODO: Somente acessivel pelo usuario administrador
    if Aluno.objects.filter(id=uid).exists() and request.user.is_authenticated:
        Aluno.objects.get(id=uid).delete()
        return HttpResponse("Aluno Deletado com Sucesso.")
    else: 
        url_anterior = request.META.get('HTTP_REFERER')
        messages.add_message(request, messages.ERROR, 'Aluno não encontrado')
        return redirect(url_anterior)

def detalhes_aluno(request:HttpRequest, uid:int):
    if request.method == 'GET' and request.user.is_authenticated:
        template_name = 'admin/dashboard_admin_detalhes_usuarios.html'
        usuario = request.user
        if user_is_aluno(usuario) or user_is_funcionario(usuario) or request.user.is_staff: 
            return render(
                request, 
                template_name, 
                context={
                    'aluno': Aluno.objects.get(id=uid)
                    }
                )
        else: 
            url_anterior = request.META.get('HTTP_REFERER')
            messages.add_message(request, messages.ERROR, 'Usuario não tem permissão para acessar essa pagina')
            return redirect(url_anterior)
    else:
        url_anterior = request.META.get('HTTP_REFERER')
        messages.add_message(request, messages.ERROR, 'Usuario não autenticado')
        return redirect(url_anterior)


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
