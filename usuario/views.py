from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from usuario.forms import LoginForm, FormularioAluno
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuario.models import Aluno, Professor, Funcionario
# from livro.models import Livro, Autor, Categoria, Reserva, Emprestimo
# from curso.models import Curso
# from django.core.paginator import Paginator
from utils.utils import *

# TODO: Essa view só pode ser acessada se o usuário estiver logado
def index(request:HttpRequest):
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
        # Carrega página de login
        formulario = LoginForm()
        return render(
            request, 
            template_name=template, 
            context={'form':formulario}
            )
    if request.method == 'POST':
        # Faz login na plataforma
        formularioLogin = LoginForm(request.POST)
        if formularioLogin.is_valid():
            usuario_formulario = formularioLogin['usuario']
            senha_formulario = formularioLogin["senha"]
            usuario = authenticate(
                username = usuario_formulario, 
                password = senha_formulario
            )
            if usuario is None:
                pass
            else:
                tipo_usuario = retorna_instancia_usuario(usuario) # type: ignore
                # TODO: Adicionar links dos templates de aluno, professor e 
                #       funcionario
                # TODO: Implementar uma função 'pegar_informacoes' que irá retor-
                #       nar todas as informações de usuário daquele usuário.
                #       - Informações de Aluno, Professor ou Funcionario [x]
                #       - Informações de emprestimos [x]
                #       - Informações de reservas [x]
                # TODO: Implementar função que verifica se esse usuário está em 
                #       débito
                template_name_aluno = "usuario/aluno/index.html"
                template_name_professor = "usuario/professor/index.html"
                template_name_funcionario = "usuario/funcionario/index.html"
                if isinstance(tipo_usuario, Aluno):
                    try:
                        login(request,usuario)
                        messages.add_message(
                            request, 
                            messages.SUCCESS, 
                            f'{usuario.username} logado com sucesso.' # type: ignore
                        ) 
                        data_context = pegar_informacoes_aluno(tipo_usuario)
                        return render(request, template_name_aluno, context=data_context)
                    except Exception as e:
                        messages.add_message(
                            request, 
                            messages.ERROR, 
                            'Erro ao fazer login. Tente novamente mais tarde.'
                        )
                        # TODO: Salvar o erro num arquivo de log
                        print(e)
                        return redirect('usuario:index') 
                elif isinstance(tipo_usuario, Professor):
                    try:
                        login(request,usuario)
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            f'{usuario.username} logado com sucesso.' # type: ignore
                        )
                        data_context = pegar_informacoes_professor(tipo_usuario)
                        return render(request, template_name_professor, context=data_context)
                    except Exception as e:
                        # TODO: Salvar o erro num arquivo de log
                        print(e)
                        messages.add_message(
                            request,
                            messages.ERROR,
                            'Erro ao fazer login. Tente novamente mais tarde.'
                        )
                        return redirect('usuario:index')
                elif isinstance(tipo_usuario, Funcionario):
                    try:
                        login(request,usuario)
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            f'{usuario.username} logado com sucesso.' # type: ignore
                        )
                        data_context = pegar_informacoes_funcionario(tipo_usuario)
                        return render(request, template_name_funcionario, context=data_context)
                    except Exception as e:
                        # TODO: Salvar o erro num arquivo de log
                        print(e)
                        messages.add_message(
                            request,
                            messages.ERROR,
                            'Erro ao fazer login. Tente novamente mais tarde.'
                        )
                        return redirect('usuario:index')
                elif usuario.is_staff(): # type: ignore
                    # Usuário é administrador
                    # FIXME: Aqui pode causar algum problema futuramente
                    messages.add_message(
                        request,
                        messages.INFO,
                        'O usuário informado é um administrador. Por favor, faça login na página de administrador.'
                    )
                    return render(
                        request,
                        template_name='usuario/redirecionar_para_administrador.html'
                    )
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Usuário não encontrado.'
                    )
                    return redirect("usuario:index")


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
                # retorna para página de login com um código de erro
                messages.error(request, 'Usuário não autorizado.')
                return redirect('usuario:entrar')
            # Faz login e retorna a página inicial da aplicação
            # Mostra mensagem de sucesso no login
            login(request, usuario)
            usuario = User.objects.get(username=formularioLogin['usuario'])
            tipo_usuario = retorna_instancia_usuario(usuario)
            messages.info(request, f'{formularioLogin.cleaned_data["usuario"]} logado com Sucesso')
            if isinstance(tipo_usuario, Aluno):
                # RETORNA A PÁGINA DE USUÁRIO DE ALUNO
                return redirect('usuario:index')
            if isinstance(tipo_usuario, Professor):
                # RETORNA A PÁGINA DE USUÁRIO DE PROFESSOR
                return redirect('usuario:index')
            if isinstance(tipo_usuario, Funcionario):
                # RETORNA A PÁGINA DE USUÁRIO DE FUNCIONARIO
                return redirect('usuario:index')
            # TODO: Se o usuário for administrador, retorna a página de administrador
            
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
    if request.method == 'GET' and request.user.is_authenticated:
        # TODO: Implementar o template abaixo
        template_name = 'usuario/professor/criar_professor.html'
        formulario_professor = FormularioProfessor()
        return render(request, template_name, context={'form': formulario_professor})
    if request.method == 'POST':
        # TODO: Implementar a regra de POST da view
        pass

def ler_professor(request:HttpRequest, uid:int):
    if request.method == 'GET' and request.user.is_authenticated:
        # TODO: Implementar o template abaixo
        template_name = 'usuario/professor/detalhes_professor.html'
        professor_existe = Professor.objects.filter(id=uid).exists()
        if professor_existe:
            professor = Professor.objects.get(id=uid)
            return render(request, template_name, context={'professor': professor})
        else:
            messages.add_message(request, messages.ERROR, 'O usuário solicitado nao existe na base de dados')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior)
    else:
        messages.add_message(request, messages.ERROR, 'O usuário nao esta logado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior)

def atualizar_professor(request:HttpRequest, uid:int):
    pass

def deletar_professor(request:HttpRequest, uid:int):
    if request.method == 'GET' and request.user.is_authenticated:
        professor_existe = Professor.objects.filter(id=uid).exists()
        if professor_existe:
            professor = Professor.objects.get(id=uid)
            professor.delete()
            messages.add_message(request, messages.SUCCESS, 'Professor deletado com sucesso.')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior)
        else: 
            messages.add_message(request, messages.ERROR, 'O usuario solicitado não existe na base de dados.')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior)
    else:
        messages.add_message(request, messages.ERROR, 'O usuario nao esta autenticado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior)

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
