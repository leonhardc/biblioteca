from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuario.forms import LoginForm, FormularioAluno
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuario.models import Aluno, Professor, Funcionario
from livro.models import Livro, Autor, Categoria, Reserva, Emprestimo
from curso.models import Curso
from django.core.paginator import Paginator


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
        return render(request, 'dashboard-admin-2.html')
    
def admin_page(request, model_type):
    if request.method == 'GET':
        if model_type=='usuarios':
            """
                Checa se a entidade selecionada no template é do tipo 'usuário', se for, faz as seguintes operações:
                1. Seleciona todos os usuarios alunos, professores e funcionários
                2. Conta o total de cada um desses tipos de usuários
                3. Faz uma paginação de acordo com o tipo de usuário e a página selecionada no template
                4. Retorna os dados de usuários requeridos no template.
            """
            alunos = Aluno.objects.all()
            professores = Professor.objects.all()
            funcionarios = Funcionario.objects.all()
            contador = {
                'alunos':len(alunos),
                'professores':len(professores),
                'funcionarios':len(funcionarios)
            }
            paginador_alunos = Paginator(alunos, 20) # 20 alunos por página
            paginador_professores = Paginator(professores, 20) # 20 professores por página
            paginador_funcionarios = Paginator(funcionarios, 20) # 20 funcionarios por página
            numero_da_pagina = request.GET.get('page')
            tipo_de_endidade = request.GET.get('type')

            if numero_da_pagina and tipo_de_endidade=='aluno':
                alunos = paginador_alunos.get_page(numero_da_pagina)
                professores = paginador_professores.get_page(1)
                funcionarios = paginador_funcionarios.get_page(1)
            elif numero_da_pagina and tipo_de_endidade=='professor':
                professores = paginador_professores.get_page(numero_da_pagina)
                alunos = paginador_alunos.get_page(1)
                funcionarios = paginador_funcionarios.get_page(1)
            elif numero_da_pagina and tipo_de_endidade=='funcionario':
                funcionarios = paginador_funcionarios.get_page(numero_da_pagina)
                alunos = paginador_alunos.get_page(1)
                professores = paginador_professores.get_page(1)
            else:
                numero_da_pagina = 1
                alunos = paginador_alunos.get_page(numero_da_pagina)
                professores = paginador_professores.get_page(numero_da_pagina)
                funcionarios = paginador_funcionarios.get_page(numero_da_pagina)
            
            return render(
                    request, 
                    'dashboard-admin-2.html', 
                    context={'usuarios':{'alunos':alunos, 'professores':professores, 'funcionarios':funcionarios}, 'contador':contador}
                )
        
        elif model_type=='livros':
            livros = Livro.objects.all()
            autores = Autor.objects.all()
            categorias = Categoria.objects.all()
            reservas = Reserva.objects.all()
            emprestimos = Emprestimo.objects.all()
            contador = {
                'livros':len(livros),
                'autores':len(autores),
                'categorias':len(categorias),
                'reservas':len(reservas),
                'emprestimos':len(emprestimos),
            }
            paginador_livros = Paginator(livros, 20)
            paginador_autores = Paginator(autores, 20)
            paginador_categorias = Paginator(categorias, 20)
            paginador_reservas = Paginator(reservas, 20)
            paginador_emprestimos = Paginator(emprestimos, 20)
            numero_da_pagina = request.GET.get('page')
            tipo_de_endidade = request.GET.get('type')
            livros = paginador_livros.get_page(1)
            autores = paginador_autores.get_page(1)
            categorias = paginador_categorias.get_page(1)
            reservas = paginador_reservas.get_page(1)
            emprestimos = paginador_emprestimos.get_page(1)
            if numero_da_pagina and tipo_de_endidade == 'livro':
                livros = paginador_livros.get_page(numero_da_pagina)
            elif numero_da_pagina and tipo_de_endidade == 'autor':
                autores = paginador_autores.get_page(numero_da_pagina)
            elif numero_da_pagina and tipo_de_endidade == 'categoria':
                categorias = paginador_categorias.get_page(numero_da_pagina)
            if numero_da_pagina and tipo_de_endidade == 'reserva':
                reservas = paginador_reservas.get_page(numero_da_pagina)
            if numero_da_pagina and tipo_de_endidade == 'emprestimo':
                emprestimos = paginador_emprestimos.get_page(numero_da_pagina)
            return render(
                    request, 
                    'dashboard-admin-2.html', 
                    context={'livros':{'livros':livros, 'autores':autores, 'categorias':categorias, 'reservas':reservas, 'emprestimos':emprestimos}, 'contador':contador}
                )
        elif model_type=='cursos':
            cursos = Curso.objects.all()
            contador = {'cursos':len(cursos)}
            paginador_cursos = Paginator(cursos, 20)
            cursos = paginador_cursos.get_page(request.GET.get('page'))
            return render(request, 'dashboard-admin-2.html',context={'cursos':cursos, 'contador':contador})
        else:
            pass

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
