from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from usuario.models import Aluno, Professor, Funcionario
from django.contrib.auth.models import User
from livro.models import Livro, Autor, Categoria, Reserva, Emprestimo
from usuario.forms import FormularioAluno, FormularioProfessor, FormularioFuncionario
from curso.models import Curso
from utils.utils import *
# Create your views here.
# Views de administrador
def dashboard_admin(request):
    if request.method == 'GET':
        template_name = 'admin/dashboard-admin.html'
        return render(request, template_name)

def dashboard_admin_usuarios(request):
    template_name = 'admin/dashboard_admin_usuarios.html'
    if request.method == 'GET':
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
                template_name, 
                context={'usuarios':{'alunos':alunos, 'professores':professores, 'funcionarios':funcionarios}, 'contador':contador}
            )

def informacoes_aluno(request, uid):
    if request.method == 'GET':
        template_name = 'admin/dashboard_admin_detalhes_usuarios.html'
        aluno = Aluno.objects.get(id=uid)
        contexto = {'aluno': aluno}
        return render(request, template_name, context=contexto)

def atualizar_infomacoes_aluno(request, uid):
    """ Em desenvolvimento """
    if request.method == "GET":
        template_name = "admin/dashboard_admin_atualizar_aluno.html"
        aluno = Aluno.objects.get(id=uid)
        endereco = separar_endereco(aluno.endereco)
        data = informacoes_formulario_aluno(aluno, endereco)
        formulario = FormularioAluno(initial=data)
        return render(request, template_name, context={"form": formulario, 'aluno': aluno})
    if request.method == "POST":
        formulario = FormularioAluno(request.POST)
        if formulario.is_valid():
            # Salvar os dados do formulário no banco de dados
            aluno = Aluno.objects.get(id = uid)
            if aluno:
                usuario = User.objects.get(id = aluno.usuario.id)
                # Salvando os dados do formulário no banco de dados
                usuario.first_name = formulario.cleaned_data['nome']
                usuario.last_name = formulario.cleaned_data['sobrenome']
                usuario.email = formulario.cleaned_data['email']
                usuario.username = formulario.cleaned_data['usuario']
                aluno.endereco = formatar_endereco(formulario)
                aluno.curso = Curso.objects.get(cod_curso = formulario.cleaned_data['curso'])
                aluno.matricula = formulario.cleaned_data['matricula']
                aluno.ingresso = formulario.cleaned_data['ingresso']
                aluno.conclusao_prevista = formulario.cleaned_data['conclusao_prevista']
                usuario.save()
                aluno.save()
                # Adicionar mensagem de sucesso!
                return redirect(f'/administrador/informacoes-aluno/{uid}/')
        else:
            # TODO: adicionar mensagem de erro
            return redirect(f'/administrador/informacoes-aluno/{uid}/')
        
def informacoes_professor(request, uid):
    if request.method=='GET':
        template_name = 'admin/dashboard_admin_detalhes_usuarios.html'
        professor = Professor.objects.get(id=uid)
        contexto = {}
        contexto['professor'] = professor
        return render(request, template_name, context=contexto)

def atualizar_informacoes_professor(request, uid):
    """ Em desenvolvimento """
    if request.method == 'GET':
        template_name = "admin/dashboard_admin_atualizar_professor.html"
        professor = Professor.objects.get(id=uid)
        data = informacoes_formulario_professor(professor)
        formulario = FormularioProfessor(initial=data)
        return render(request, template_name, context={"form": formulario, 'professor':professor})
        pass
    if request.method == 'POST':
        # Implementar o método POST e salvar os dados alterados no banco de dados
        # Lembrar de validar os dados antes de salvar no banco de dados
        pass

def informacoes_funcionario(request, uid):
    if request.method=='GET':
        template_name = 'admin/dashboard_admin_detalhes_usuarios.html'
        funcionario = Funcionario.objects.get(id=uid)
        contexto = {}
        contexto['funcionario'] = funcionario
        return render(request, template_name, context=contexto)

def atualizar_informacoes_funcionario(request, uid):
    if request.method == "GET":
        template_name = 'admin/dashboard_admin_atualizar_funcionario.html'
        funcionario = Funcionario.objects.get(id=uid)
        data = informacoes_formulario_funcionario(funcionario)
        formulario = FormularioFuncionario(initial=data)
        return render(request, template_name, context={"form": formulario, 'funcionario':funcionario})
        pass
    if request.method == "POST":
        # Implementar o método POST e salvar os dados alterados no banco de dados
        # Lembrar de validar os dados antes de salvar no banco de dados
        pass

def deletar_aluno(request, uid):
    pass

def deletar_professor(request, uid):
    pass

def deletar_funcionario(request, uid):
    pass

def dashboard_admin_livros(request):
    template_name = 'admin/dashboard_admin_livros.html'
    if request.method == 'GET':
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
                template_name, 
                context={'livros':{'livros':livros, 'autores':autores, 'categorias':categorias, 'reservas':reservas, 'emprestimos':emprestimos}, 'contador':contador}
            )

def dashboard_admin_cursos(request):
    template_name = 'admin/dashboard_admin_cursos.html'
    if request.method == 'GET':
        cursos = Curso.objects.all()
        contador = {'cursos':len(cursos)}
        paginador_cursos = Paginator(cursos, 20)
        cursos = paginador_cursos.get_page(request.GET.get('page'))
        return render(request, template_name,context={'cursos':cursos, 'contador':contador})
