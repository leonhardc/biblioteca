from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuario.forms import LoginForm, FormularioAluno
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuario.models import Aluno, Professor, Funcionario
from livro.models import Livro, Autor, Categoria
from curso.models import Curso


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

# Views de administrador
def dashboard_admin(request):
    if request.method == 'GET':
        alunos = Aluno.objects.all()
        professores = Professor.objects.all()
        funcionarios = Funcionario.objects.all()
        livros = Livro.objects.all()
        autores = Autor.objects.all()
        categorias = Categoria.objects.all()
        cursos = Curso.objects.all()
        contadores_de_query = {
            'alunos': len(alunos),
            'professores': len(professores),
            'funcionarios': len(funcionarios),
            'livros': len(livros),
            'autores': len(autores),
            'categorias': len(categorias),
            'cursos': len(cursos),
        }
        return render(request, 'dashboard-admin.html', context={'contador':contadores_de_query})
                      
def admin_page(request, model_type):
    if request.method == 'GET':
        alunos = Aluno.objects.all()
        professores = Professor.objects.all()
        funcionarios = Funcionario.objects.all()
        livros = Livro.objects.all()
        autores = Autor.objects.all()
        categorias = Categoria.objects.all()
        cursos = Curso.objects.all()
        contadores_de_query = {
            'alunos': len(alunos),
            'professores': len(professores),
            'funcionarios': len(funcionarios),
            'livros': len(livros),
            'autores': len(autores),
            'categorias': len(categorias),
            'cursos': len(cursos),
        }
        retorno_por_tipo = {
            'aluno': render(request, 'dashboard-admin.html', context={'contador':contadores_de_query, 'alunos':alunos}),
            'professor': render(request, 'dashboard-admin.html', context={'contador':contadores_de_query, 'professores':professores}),
            'funcionario': render(request, 'dashboard-admin.html', context={'contador':contadores_de_query, 'funcionarios':funcionarios}),
            'livro': render(request, 'dashboard-admin.html', context={'contador':contadores_de_query, 'livros':livros}),
            'autor': render(request, 'dashboard-admin.html', context={'contador':contadores_de_query, 'autores':autores}),
            'categoria': render(request, 'dashboard-admin.html', context={'contador':contadores_de_query, 'categorias':categorias}),
            'curso': render(request, 'dashboard-admin.html', context={'contador':contadores_de_query, 'cursos':cursos}),
        }
        return retorno_por_tipo[model_type]

# CRUD de Aluno
def listar_alunos(request):
    query_alunos = Aluno.objects.all()
    return render(request, 'lista_alunos.html', context={'alunos':query_alunos})


def criar_aluno(request):
    if request.method == 'GET':
        formulario_aluno = FormularioAluno()
        return render(request, template_name='form.html', context={'form':formulario_aluno})
    else: 
        if request.method == 'POST':
            # TODO: Salvar as informações de usuário e aluno do formulário no banco de dados
            formulario_novo_aluno = FormularioAluno(request.POST)
            # TODO: Implementar página de retorno com mensagem de sucesso
            if formulario_novo_aluno.is_valid():
                return HttpResponse('OK')
            else:
                return render(request, template_name='formulario-cadastro-aluno.html', context={'form':formulario_novo_aluno})
    

def ler_aluno(request, uid):
    # Página de detalhes de aluno
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
