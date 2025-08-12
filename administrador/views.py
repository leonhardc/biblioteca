from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpRequest
from django.core.paginator import Paginator
from usuario.models import Aluno, Professor, Funcionario
from django.contrib.auth.models import User
from django.contrib import messages
from livro.models import Livro, Autor, Categoria, Reserva, Emprestimo
from usuario.forms import FormularioAluno, FormularioProfessor, FormularioFuncionario
from livro.forms import FormularioLivro, FormularioAutor, FormularioCategoria, FormularioReserva, FormularioCriarEmprestimo, FormularioAtualizarEmprestimo
from curso.forms import FormularioCurso
from curso.models import Curso
from utils.utils import *
from utils.formularios.utils_formularios import *

# Views de administrador

# TODO: Atualizar todas as funções update para receber o método 'UPDATE' na submissão do formulário

def dashboard_admin(request: HttpRequest):
    template_name = 'admin/dashboard_admin_home.html'
    if request.method == 'GET':
        dict_usuarios = { # type: ignore
            'alunos': Aluno.objects.all(),
            'professores': Professor.objects.all(),
            'funcionarios': Funcionario.objects.all()
        }
        dict_livros = { # type: ignore
            'livros': Livro.objects.all(),
            'autores': Autor.objects.all(),
            'categorias': Categoria.objects.all(),
            'reservas': Reserva.objects.all(),
            'emprestimos': Emprestimo.objects.all(),
        }
        dict_cursos = { # type: ignore
            'cursos': Curso.objects.all(),
        }
        contadores = { # type: ignore
            'alunos': len(dict_usuarios['alunos']), # type: ignore
            'professores': len(dict_usuarios['professores']), # type: ignore
            'funcionarios': len(dict_usuarios['funcionarios']), # type: ignore
            'livros': len(dict_livros['livros']), # type: ignore
            'autores': len(dict_livros['autores']), # type: ignore
            'categorias': len(dict_livros['categorias']), # type: ignore
            'reservas': len(dict_livros['reservas']), # type: ignore
            'emprestimos': len(dict_livros['emprestimos']), # type: ignore
            'cursos': len(dict_cursos['cursos']), # type: ignore
            'todos_usuarios': len(dict_usuarios['alunos']) + len(dict_usuarios['professores']) + len(dict_usuarios['funcionarios']) # type: ignore
        }
        return render(
            request, 
            template_name,
            context={
                # 'usuarios': dict_usuarios,
                # 'livros': dict_livros,
                # 'cursos': dict_cursos,
                'contadores': contadores,
            }
        )

# Usuários: dashboard e crud


def dashboard_admin_usuarios(request: HttpRequest):
    template_name = 'admin/usuario/dashboard_admin_usuarios.html'
    if request.method == 'GET':
        alunos = Aluno.objects.all()
        professores = Professor.objects.all()
        funcionarios = Funcionario.objects.all()
        contador = {
            'alunos': len(alunos),
            'professores': len(professores),
            'funcionarios': len(funcionarios)
        }
        paginador_alunos = Paginator(alunos, 20) # type: ignore # 20 alunos por página
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
                context={'usuarios': {'alunos': alunos, 'professores': professores, 'funcionarios': funcionarios}, 'contador': contador}
            )

# views de Alunos


def criar_aluno(request: HttpRequest):
    template_name = "admin/usuario/dashboard_admin_criar_aluno.html"
    if request.method == 'GET':
        formulario = FormularioAluno()
        return render(request, template_name, context={'form': formulario})
    if request.method == 'POST':
        formulario = FormularioAluno(request.POST)
        if formulario.is_valid():
            usuario_existe = User.objects.filter(
                Q(username=formulario.cleaned_data['usuario']) |
                Q(email=formulario.cleaned_data['usuario'])
            ).exists()
            if not usuario_existe:
                aluno_existe = Aluno.objects.filter(cpf=formulario.cleaned_data['cpf']).exists()
                if not aluno_existe:
                    # criar novo usuario
                    try:
                        usuario=User.objects.create_user(
                            username=formulario.cleaned_data['usuario'],
                            first_name=formulario.cleaned_data['nome'],
                            last_name=formulario.cleaned_data['sobrenome'],
                            email=formulario.cleaned_data['email'],
                            password='1234'
                        )
                        curso = Curso.objects.get(cod_curso=formulario.cleaned_data['curso'])
                        Aluno.objects.create(
                            usuario = usuario,
                            matricula = gerar_matricula_aluno(),
                            curso = curso,
                            endereco = formatar_endereco(formulario),
                            cpf = formulario.cleaned_data['cpf'],
                            ingresso = formulario.cleaned_data['ingresso'],
                            conclusao_prevista = formulario.cleaned_data['conclusao_prevista'],
                        )
                        messages.add_message(request, messages.SUCCESS, 'Aluno adicionado com sucesso.')
                        return redirect('/administrador/usuarios/')
                    except Exception as e:
                        messages.add_message(request, messages.ERROR, f'Erro ao criar Usuário ou Aluno:\n{e}')
                        return redirect('/administrador/usuarios/')
                else:
                    messages.add_message(request, messages.ERROR, 'O Aluno já existe na base de dados.')
                    return render(request, template_name, context={'form':formulario})
            else: 
                messages.add_message(request, messages.ERROR, 'A base de dados já contem esse usuário ou um usuário com esse email.')
                return render(request, template_name, context={'form':formulario})
        else:
            # Retorna o formulário com mensagem de erro
            messages.add_message(request, messages.ERROR, 'Problemas ao salvar os dados do formulario no banco de dados.')
            return render(request, template_name, context={'form':formulario})


def informacoes_aluno(request: HttpRequest, uid: int):
    if request.method == 'GET':
        template_name = 'admin/usuario/dashboard_admin_detalhes_usuarios.html'
        aluno = Aluno.objects.filter(id=uid).exists()
        if aluno:
            aluno = Aluno.objects.get(id=uid)
            reservas = Reserva.objects.filter(usuario=aluno.usuario)            # type: ignore
            emprestimos = Emprestimo.objects.filter(usuario=aluno.usuario)      # type: ignore
            contexto = {'aluno': aluno, 'reservas': reservas, 'emprestimos':emprestimos} # type: ignore
            return render(request, template_name, context=contexto)             # type: ignore
        else:
            messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
            return redirect('/administrado/usuarios/')


def atualizar_infomacoes_aluno(request: HttpRequest, uid: int):
    """ Em desenvolvimento """
    template_name = "admin/usuario/dashboard_admin_atualizar_aluno.html"
    if request.method == "GET":
        aluno_existe = Aluno.objects.filter(id=uid).exists()
        if aluno_existe:
            aluno = Aluno.objects.get(id=uid)
            endereco = separar_endereco(aluno.endereco) # type: ignore
            data = informacoes_formulario_aluno(aluno, endereco)
            formulario = FormularioAluno(initial=data)
            return render(request, template_name, context={"form": formulario, 'aluno': aluno})
        else:
            messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
            return redirect('/administrado/usuarios/')
    if request.method == "POST":
        formulario = FormularioAluno(request.POST)
        if formulario.is_valid():
            aluno_existe = Aluno.objects.filter(id = uid).exists()
            if aluno_existe:
                aluno:Aluno = Aluno.objects.get(id = uid)
                usuario:User = aluno.usuario # type: ignore
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
                usuario.save() # type: ignore
                aluno.save()
                messages.add_message(request, messages.SUCCESS, 'Os dados foram salvos com sucesso.')
                return redirect(f'/administrador/informacoes-aluno/{uid}/')
            else:
                messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
                return redirect(f'/administrador/informacoes-aluno/{uid}/')
        else:
            aluno = Aluno.objects.get(id=uid)
            return render(request, template_name, context={"form": formulario, 'aluno': aluno})


def deletar_aluno(request: HttpRequest, uid: int):
    aluno = Aluno.objects.filter(id=uid).exists()
    if aluno:
        aluno = Aluno.objects.get(id=uid)
        aluno.delete()
        messages.add_message(request, messages.SUCCESS, f'Aluno deletado com sucesso.')
        return redirect('/administrador/usuarios/')
    else: 
        messages.add_message(request, messages.ERROR, f'Erro ao deletar o Aluno.')
        return redirect('/administrador/usuarios/')

# views de Professores


def criar_professor(request: HttpRequest):
    template_name = "admin/usuario/dashboard_admin_criar_professor.html"
    if request.method == 'GET':
        formulario = FormularioProfessor()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioProfessor(request.POST)
        if formulario.is_valid():
            usuario = User.objects.filter(
                Q(username=formulario.cleaned_data['usuario']) |
                Q(email=formulario.cleaned_data['email']) 
            ).exists()
            if not usuario:
                professor = Professor.objects.filter(cpf=formulario.cleaned_data['cpf']).exists()
                if not professor:
                    try:
                        usuario = User.objects.create_user(
                            username = formulario.cleaned_data['usuario'],
                            first_name = formulario.cleaned_data['nome'],
                            last_name =  formulario.cleaned_data['sobrenome'],
                            email = formulario.cleaned_data['email'],
                            password = '1234'
                        )
                        curso = Curso.objects.get(cod_curso=formulario.cleaned_data['curso'])
                        professor = Professor.objects.create(
                            usuario = usuario, 
                            matricula = gerar_matricula_professor(),
                            curso = curso,
                            cpf = formulario.cleaned_data['cpf'],
                            regime = formulario.cleaned_data['regime'],
                            contratacao = formulario.cleaned_data['contratacao']
                        )
                        messages.add_message(request, messages.SUCCESS, 'Professor adicionado com sucesso.')
                        return redirect('/administrador/usuarios/')
                    except Exception as e:
                        messages.add_message(request, messages.ERROR, f'Erro ao criar Usuário ou Professor.\n{e}')
                        return redirect('/administrador/usuarios/')
                else:
                    messages.add_message(request, messages.ERROR, 'Professor já existe na base de dados.')
                    return render(request, template_name, context={'form':formulario})
            else:
                messages.add_message(request, messages.ERROR, 'A base de dados já contem esse usuário ou um usuário com esse email.')
                return render(request, template_name, context={'form':formulario})
        else:
            messages.add_message(request, messages.ERROR, 'Problemas ao salvar os dados do formulario no banco de dados.')
            return render(request, template_name, context={'form':formulario})


def informacoes_professor(request: HttpRequest, uid: int):
    template_name = 'admin/usuario/dashboard_admin_detalhes_usuarios.html'
    if request.method=='GET':
        professor = Professor.objects.filter(id=uid).exists()
        if professor:
            professor = Professor.objects.get(id=uid)
            reservas = Reserva.objects.filter(usuario=professor.usuario)            # type: ignore
            emprestimos = Emprestimo.objects.filter(usuario=professor.usuario)      # type: ignore
            contexto = {'professor':professor, 'reservas': reservas, 'emprestimos': emprestimos}  # type: ignore
            return render(request, template_name, context=contexto)                 # type: ignore
        else:
            messages.add_message(request, messages.ERROR, 'Professor não encontrado.')
            return redirect('/administrador/usuarios/')


def atualizar_informacoes_professor(request: HttpRequest, uid: int):
    """ Em desenvolvimento """
    template_name = "admin/usuario/dashboard_admin_atualizar_professor.html"
    if request.method == 'GET':
        professor_existe = Professor.objects.filter(id=uid).exists()
        if professor_existe:
            professor = Professor.objects.get(id=uid)
            data = informacoes_formulario_professor(professor)
            formulario = FormularioProfessor(initial=data)
            return render(request, template_name, context={"form": formulario, 'professor':professor})
        else:
            messages.add_message(request, messages.ERROR, 'Professor não encontrado.')
            return redirect('/administrador/usuarios/')
    if request.method == 'POST':
        formulario = FormularioProfessor(request.POST)
        if formulario.is_valid():
            professor_existe = Professor.objects.filter(id=uid).exists()
            if professor_existe:
                professor:Professor = Professor.objects.get(id=uid)
                usuario:User = professor.usuario # type: ignore
                # Salvando os dados do formulário no banco de dados
                usuario.first_name = formulario.cleaned_data['nome']
                usuario.last_name = formulario.cleaned_data['sobrenome']
                usuario.email = formulario.cleaned_data['email']
                usuario.username = formulario.cleaned_data['usuario']
                professor.curso = Curso.objects.get(cod_curso = formulario.cleaned_data['curso'])
                professor.matricula = formulario.cleaned_data['matricula']
                professor.cpf = formulario.cleaned_data['cpf']
                professor.regime = formulario.cleaned_data['regime']
                professor.contratacao = formulario.cleaned_data['contratacao']
                usuario.save() # type: ignore
                professor.save()
                messages.add_message(request, messages.SUCCESS, 'Os dados foram salvos com sucesso.')
                return redirect(f'/administrador/informacoes-professor/{uid}/')
            else:
                messages.add_message(request, messages.ERROR, 'Professor não encontrado.')
                return redirect(f'/administrador/informacoes-professor/{uid}/')
        else: 
            professor = Professor.objects.get(id=uid)
            return render(request, template_name, context={"form": formulario, 'professor': professor})


def deletar_professor(request: HttpRequest, uid: int):
    professor = Professor.objects.filter(id=uid).exists()
    if professor:
        professor = Professor.objects.get(id=uid)
        professor.delete()
        messages.add_message(request, messages.SUCCESS, f'Professor deletado com sucesso.')
        return redirect('/administrador/usuarios/')
    else:
        messages.add_message(request, messages.ERROR, f'Erro ao deletar Professor.')
        return redirect('/administrador/usuarios/')

# views de Funcionarios

def criar_funcionario(request: HttpRequest):
    template_name = 'admin/usuario/dashboard_admin_criar_funcionario.html'
    if request.method == 'GET':
        formulario = FormularioFuncionario()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioFuncionario(request.POST)
        if formulario.is_valid():
            usuario = User.objects.filter(
                Q(username=formulario.cleaned_data['usuario'])|
                Q(email=formulario.cleaned_data['email'])
            ).exists()
            if not usuario:
                funcionario = Funcionario.objects.filter(cpf=formulario.cleaned_data['cpf']).exists()
                if not funcionario:
                    try:
                        usuario = User.objects.create_user(
                            username = formulario.cleaned_data['usuario'],
                            first_name = formulario.cleaned_data['nome'],
                            last_name =  formulario.cleaned_data['sobrenome'],
                            email = formulario.cleaned_data['email'],
                            password = '1234'
                        )
                        funcionario = Funcionario.objects.create(
                            usuario = usuario,
                            matricula = gerar_matricula_funcionario(),
                            cpf = formulario.cleaned_data['cpf']
                        )
                        messages.add_message(request, messages.SUCCESS, f'Funcionario criado com sucesso.')
                        return redirect('/administrador/usuarios/')
                    except Exception as e:
                        messages.add_message(request, messages.ERROR, f'Erro ao criar Usuário ou Funcionario.\n{e}')
                        return redirect('/administrador/usuarios/')
                else:
                    messages.add_message(request, messages.ERROR, 'Funcionário já existe na base de dados.')
                    return render(request, template_name, context={'form':formulario})
            else:
                messages.add_message(request, messages.ERROR, 'A base de dados já contem esse usuário ou um usuário com esse email.')
                return render(request, template_name, context={'form':formulario})
        else:
            messages.add_message(request, messages.ERROR, 'Problemas ao salvar os dados do formulario no banco de dados.')
            return render(request, template_name, context={'form':formulario})


def informacoes_funcionario(request: HttpRequest, uid: int):
    if request.method=='GET':
        template_name = 'admin/usuario/dashboard_admin_detalhes_usuarios.html'
        funcionario = Funcionario.objects.get(id=uid)
        reservas = Reserva.objects.filter(usuario=funcionario.usuario)            # type: ignore
        emprestimos = Emprestimo.objects.filter(usuario=funcionario.usuario)      # type: ignore
        contexto = {'funcionario': funcionario, 'reservas': reservas, 'emprestimos': emprestimos} # type: ignore
        return render(request, template_name, context=contexto) # type: ignore


def atualizar_informacoes_funcionario(request: HttpRequest, uid: int):
    template_name = 'admin/usuario/dashboard_admin_atualizar_funcionario.html'
    if request.method == "GET":
        funcionario = Funcionario.objects.filter(id=uid).exists()
        if funcionario:
            funcionario = Funcionario.objects.get(id=uid)
            data = informacoes_formulario_funcionario(funcionario)
            formulario = FormularioFuncionario(initial=data)
            return render(request, template_name, context={"form": formulario, 'funcionario':funcionario})
        else:
            messages.add_message(request, messages.ERROR, 'Funcionário não encontrado.')
            return redirect('/administrador/usuarios/')
    if request.method == "POST":
        formulario = FormularioFuncionario(request.POST)
        if formulario.is_valid():
            funcionario = Funcionario.objects.filter(id=uid).exists()
            if funcionario:
                funcionario = Funcionario.objects.get(id=uid)
                usuario:User = funcionario.usuario # type: ignore
                # Salvando os dados do formulário no banco de dados
                usuario.first_name = formulario.cleaned_data['nome']
                usuario.last_name = formulario.cleaned_data['sobrenome']
                usuario.email = formulario.cleaned_data['email']
                usuario.username = formulario.cleaned_data['usuario']
                funcionario.matricula = formulario.cleaned_data['matricula']
                funcionario.cpf = formulario.cleaned_data['cpf']
                usuario.save() # type: ignore
                funcionario.save()
                messages.add_message(request, messages.SUCCESS, 'Os dados foram salvos com sucesso.')
                return redirect(f'/administrador/informacoes-funcionario/{uid}/')
            else:
                messages.add_message(request, messages.ERROR, 'Funcionario não encontrado.')
                return redirect(f'/administrador/informacoes-funcionario/{uid}/')
        else:
            funcionario = Funcionario.objects.get(id=uid)
            return render(request, template_name, context={"form": formulario, 'funcionario': funcionario})


def deletar_funcionario(request: HttpRequest, uid: int):
    funcionario = Funcionario.objects.filter(id=uid).exists()
    if funcionario:
        funcionario = Funcionario.objects.get(id=uid)
        funcionario.delete()
        messages.add_message(request, messages.SUCCESS, f'Aluno deletado com sucesso.')
        return redirect('/administrador/usuarios/')
    else:
        messages.add_message(request, messages.ERROR, f'Erro ao deletar Funcionario.')
        return redirect('/administrador/usuarios/')

# Livros: dashboard e crud

# Views de Livros


def dashboard_admin_livros(request: HttpRequest):
    template_name = 'admin/livro/dashboard_admin_livros.html'
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


def criar_livro(request: HttpRequest):
    template_name = 'admin/livro/dashboard_admin_criar_livro.html'
    if request.method == 'GET':
        formulario = FormularioLivro()
        return render(request,template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioLivro(request.POST)
        if formulario.is_valid():
            livro_exite = Livro.objects.filter(isbn=formulario.cleaned_data['isbn']).exists()
            if not livro_exite:
                try:
                    livro:Livro = Livro.objects.create(
                        isbn=formulario.cleaned_data['isbn'],
                        titulo=formulario.cleaned_data['titulo'],
                        subtitulo=formulario.cleaned_data['subtitulo'],
                        lancamento=formulario.cleaned_data['lancamento'],
                        editora=formulario.cleaned_data['editora'],
                        copias=formulario.cleaned_data['copias'],
                        categoria=formulario.cleaned_data['categoria'],
                    )
                    livro.autores.set(formulario.cleaned_data['autores']) # type: ignore
                    messages.add_message(request, messages.SUCCESS, 'Livro adicionado com sucesso.')
                    return redirect('/administrador/livros/')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f'Erro ao adicionar novo livro.\n{e}.')
                    return render(request, template_name, context={'form':formulario})
            else:
                messages.add_message(request, messages.ERROR, 'O livro já existe na base de dados.')
                return render(request, template_name, context={'form':formulario})
        else:
            messages.add_message(request, messages.ERROR, 'Não foi possível criar o livro. Formulário inválido.')
            return render(request, template_name, context={'form':formulario})


def informacoes_livro(request: HttpRequest, lid: int):
    template_name = 'admin/livro/dashboard_admin_detalhes_livros.html'
    if request.method == 'GET':
        livro = Livro.objects.filter(id=lid).exists()
        if livro:
            livro = Livro.objects.get(id=lid)
            return render(request, template_name, context={'livro':livro})
        else:
            messages.add_message(request, messages.ERROR, 'Não foi possivel encontra o livro solicitado.')
            return redirect('/administrador/livros/')


def atualizar_informacoes_livro(request: HttpRequest, lid: int):
    template_name = 'admin/livro/dashboard_admin_atualizar_livro.html'
    if request.method=='GET':
        livro_existe = Livro.objects.filter(id=lid).exists()
        if livro_existe:
            livro = Livro.objects.get(id=lid)
            data = informacoes_formulario_livro(livro)
            formulario = FormularioLivro(initial=data)
            return render(request, template_name, context={'form':formulario, 'livro':livro})
        else:
            messages.add_message(request, messages.ERROR, 'Livro não encontrado.')
            return redirect('/administrador/livros/')
    if request.method=='POST':
        formulario = FormularioLivro(request.POST)
        if formulario.is_valid():
            livro_existe:bool = Livro.objects.filter(id=lid).exists()
            if livro_existe:
                try:
                    livro:Livro = Livro.objects.get(id=lid)
                    livro.titulo = formulario.cleaned_data['titulo']
                    livro.subtitulo = formulario.cleaned_data['subtitulo']
                    livro.lancamento = formulario.cleaned_data['lancamento']
                    livro.editora = formulario.cleaned_data['editora']
                    livro.copias = formulario.cleaned_data['copias']
                    livro.autores.set(formulario.cleaned_data['autores']) # type: ignore
                    livro.categoria = formulario.cleaned_data['categoria']
                    livro.save()
                    # livro = Livro.objects.filter(id=lid).update(**formulario.cleaned_data)
                    messages.add_message(request, messages.SUCCESS, 'Livro atualizado com sucesso.')
                    return redirect('/administrador/livros/')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f'Erro ao atualizar os dados. {e}.')
                    return redirect('/administrador/livros/')
            else:
                messages.add_message(request, messages.ERROR, 'Erro ao atualizar os dados. Livro não encontrado.')
                return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Erro ao atualizar os dados. Formulário Inválido.')
            return redirect('/administrador/livros/')


def deletar_livro(request: HttpRequest, lid: int):
    if request.method == 'GET':
        livro = Livro.objects.filter(id=lid).exists()
        if livro:
            livro = Livro.objects.get(id=lid)
            livro.delete()
            messages.add_message(request, messages.INFO, 'Livro deletado com sucesso.')
            return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.INFO, 'Livro não encontrado.')
            return redirect('/administrador/livros/')

## Views de Autores

def criar_autor(request: HttpRequest):
    template_name = 'admin/livro/dashboard_admin_criar_autor.html'
    if request.method == 'GET':
        formulario = FormularioAutor()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioAutor(request.POST)
        if formulario.is_valid():
            autor = Autor.objects.filter(
                Q(nome=formulario.cleaned_data['nome']) |
                Q(cpf=formulario.cleaned_data['cpf'])
            ).exists()
            if not autor:
                try:
                    autor = Autor.objects.create(
                        nome = formulario.cleaned_data['nome'],
                        cpf = formulario.cleaned_data['cpf'],
                        nacionalidade = formulario.cleaned_data['nacionalidade'],
                    )
                    messages.add_message(request, messages.SUCCESS, 'Autor salvo com sucesso.')
                    return redirect('/administrador/livros/')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f'Erro ao salvar informações na base de dados. {e}.')
                    return redirect('/administrador/livros/')
            else:
                messages.add_message(request, messages.ERROR, 'O Autor já existe.')
                return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Erro ao salvar informações do autor. Formulário inválido.')
            return redirect('/administrador/livros/')


def informacoes_autor(request: HttpRequest, aid: int):
    template_name = 'admin/livro/dashboard_admin_detalhes_livros.html'
    if request.method=='GET':
        autor = Autor.objects.filter(id=aid).exists()
        if autor:
            autor = Autor.objects.get(id=aid)
            return render(request, template_name, context={'autor':autor})
        else:
            messages.add_message(request, messages.ERROR, 'Autor não encontrado.')
            return redirect('/administrador/livros/')


def atualizar_informacoes_autor(request: HttpRequest, aid: int):
    template_name = 'admin/livro/dashboard_admin_atualizar_autor.html'
    if request.method == 'GET':
        autor = Autor.objects.filter(id=aid).exists()
        if autor:
            autor = Autor.objects.get(id=aid)
            data = informacoes_formulario_autor(autor)
            formulario = FormularioAutor(initial=data)
            return render(request, template_name, context={'form':formulario, 'autor':autor})
        else:
            messages.add_message(request, messages.ERROR, 'O autor não foi encontrado na base de dados.')
            return redirect('/administrador/livros/')
    if request.method == 'POST':
        formulario = FormularioAutor(request.POST)
        if formulario.is_valid():
            autor = Autor.objects.filter(id=aid).exists()
            if autor:
                autor = Autor.objects.get(id=aid)
                autor.nome = formulario.cleaned_data['nome']
                autor.cpf = formulario.cleaned_data['cpf']
                autor.nacionalidade = formulario.cleaned_data['nacionalidade']
                autor.save()
                messages.add_message(request, messages.SUCCESS, 'Autor atualizado com sucesso.')
                return redirect('/administrador/livros/')
            else:
                messages.add_message(request, messages.ERROR, 'Autor não encontrado.')
                return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Formulário inválido.')
            return redirect('/administrador/livros/')


def deletar_autor(request: HttpRequest, aid: int):
    if request.method == 'GET':
        autor = Autor.objects.filter(id=aid).exists()
        if autor:
            autor = Autor.objects.get(id=aid)
            autor.delete()
            messages.add_message(request, messages.INFO, 'Autor deletado com sucesso.')
            return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Autor não encontrado.')
            return redirect('/administrador/livros/')

## Views de Categorias


def criar_categoria(request: HttpRequest):
    template_name = 'admin/livro/dashboard_admin_criar_categoria.html'
    if request.method == 'GET':
        formulario = FormularioCategoria()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioCategoria(request.POST)
        if formulario.is_valid():
            categoria_existe = Categoria.objects.filter(categoria=formulario.cleaned_data['categoria']).exists()
            if not categoria_existe:
                try:
                    Categoria.objects.create(
                        categoria = formulario.cleaned_data['categoria'],
                        descricao = formulario.cleaned_data['descricao']
                    )
                    messages.add_message(request, messages.SUCCESS, 'Categoria criada com sucesso.')
                    return redirect('/administrador/livros/')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f'Erro ao criar categoria.\n{e}')
                    return redirect('/administrador/livros/')
            else:
                messages.add_message(request, messages.ERROR, 'Categoria já existe.')
                return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Formulario Invalido.')
            return redirect('/administrador/livros/')


def informacoes_categoria(request: HttpRequest, cid: int):
    template_name = 'admin/livro/dashboard_admin_detalhes_livros.html'
    if request.method=='GET':
        categoria = Categoria.objects.filter(id=cid).exists()
        if categoria:
            categoria = Categoria.objects.get(id=cid)
            return render(request, template_name, context={'categoria':categoria})
        else:
            messages.add_message(request, messages.ERROR, 'Categoria não encontrada')
            return redirect('/administrador/livros/')


def atualizar_informacoes_categoria(request: HttpRequest, cid: int):
    template_name = 'admin/livro/dashboard_admin_atualizar_categoria.html'
    if request.method=='GET':
        categoria = Categoria.objects.filter(id=cid).exists()
        if categoria:
            categoria = Categoria.objects.get(id=cid)
            data = informacoes_formulario_categoria(categoria)
            formulario = FormularioCategoria(initial=data)
            return render(request, template_name, context={'form': formulario, 'categoria': categoria})
        else:
            messages.add_message(request, messages.ERROR, 'A categoria não existe na base de dados.')
            return redirect('/administrador/livros/')
    if request.method=='POST':
        formulario = FormularioCategoria(request.POST)
        if formulario.is_valid():
            categoria = Categoria.objects.filter(id=cid).exists()
            if categoria:
                categoria = Categoria.objects.get(id=cid)
                categoria.categoria = formulario.cleaned_data['categoria']
                categoria.descricao = formulario.cleaned_data['descricao']
                categoria.save()
                messages.add_message(request, messages.SUCCESS, 'Categoria atualizada com sucesso.')
                return redirect('/administrador/livros/')
            else:
                messages.add_message(request, messages.ERROR, 'Categoria não encontrada.')
                return redirect('/administrador/livros/')
        else: 
            messages.add_message(request, messages.ERROR, 'Formulário inválido.')
            return redirect('/administrador/livros/')


def deletar_categoria(request: HttpRequest, cid: int):
    if request.method == 'GET':
        categoria = Categoria.objects.filter(id=cid).exists()
        if categoria:
            categoria = Categoria.objects.get(id=cid)
            categoria.delete()
            messages.add_message(request, messages.INFO, 'Categoria deletada com sucesso.')
            return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Categoria não encontrada.')
            return redirect('/administrador/livros/')

## Views de Reservas


def criar_reserva(request: HttpRequest):
    template_name = 'admin/livro/dashboard_admin_criar_reserva.html'
    if request.method == 'GET':
        formulario = FormularioReserva()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioReserva(request.POST)
        if formulario.is_valid():
            reserva_existe = Reserva.objects.filter(usuario=formulario.cleaned_data['usuario'], livro=formulario.cleaned_data['livro']).exists()
            if not reserva_existe:
                try:
                    usuario = User.objects.get(id=formulario.cleaned_data['usuario'])
                    livro = Livro.objects.get(id=formulario.cleaned_data['livro'])
                    Reserva.objects.create(
                        usuario = usuario,
                        livro = livro,
                        data_reserva = formulario.cleaned_data['data_reserva']
                    )
                    messages.add_message(request, messages.SUCCESS, 'Reserva cadastrado com sucesso.')
                    return redirect('/administrador/livros/')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f'Erro ao cadastrar reserva.{e}')
                    return redirect('/administrador/livros/')
            else:
                messages.add_message(request, messages.ERROR, 'Essa reserva já existe.')
                return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Formulário Inválido.')
            return redirect('/administrador/livros/')


def informacoes_reserva(request: HttpRequest, rid: int):
    template_name = 'admin/livro/dashboard_admin_detalhes_livros.html'
    if request.method =='GET':
        reserva_existe = Reserva.objects.filter(id=rid).exists()
        if reserva_existe:
            reserva = Reserva.objects.get(id=rid)
            return render(request, template_name, context={'reserva':reserva})
        else:
            messages.add_message(request, messages.ERROR, 'Reserva não encontrada.')
            return redirect('/administrador/livros/')


def atualizar_informacoes_reserva(request: HttpRequest, rid: int):
    template_name = "admin/livro/dashboard_admin_atualizar_reserva.html"
    if request.method == 'GET':
        reserva = Reserva.objects.get(id=rid)
        if not reserva:
            messages.add_message(request, messages.ERROR, "Reserva não encontrada.")
            return redirect("/administrador/livros/")
        data = informacoes_formulario_reserva(reserva)
        formulario = FormularioReserva(initial=data)
        return render(request, template_name, context={'form':formulario, 'reserva':reserva})
    if request.method == 'POST':
        formulario = FormularioReserva(request.POST)
        if formulario.is_valid():
            reserva_existe = Reserva.objects.filter(id=rid).exists()
            if reserva_existe:
                try:
                    reserva = Reserva.objects.get(id=rid)
                    reserva.usuario = formulario.cleaned_data['usuario']
                    reserva.livro = formulario.cleaned_data['livro']
                    reserva.data_reserva = formulario.cleaned_data['data_reserva']
                    reserva.save()
                    messages.add_message(request, messages.SUCCESS, "Informações salvas com sucesso.")
                    return redirect("/administrador/livros/")
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f"Um erro aconteceu ao tentar atualizar as informações de reserva.{e}")
                    return redirect("/administrador/livros/")
            else:
                messages.add_message(request, messages.ERROR, "A reserva informada não existe.")
                return redirect("/administrador/livros/")
        else:
            messages.add_message(request, messages.ERROR, "Formulário inválido.")
            return redirect("/administrador/livros/")


def deletar_reserva(request: HttpRequest, rid: int):
    reserva_existe = Reserva.objects.filter(id=rid).exists()
    if reserva_existe:
        try:
            reserva = Reserva.objects.get(id=rid)
            reserva.delete()
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Um erro aconteceu ao tentar deletar a reserva.{e}")
            return redirect("/administrador/livros/")
    else:
        messages.add_message(request, messages.ERROR, "A reserva informada não existe.")
        return redirect("/administrador/livros/")

## Views de Emprestimos


def criar_emprestimo(request: HttpRequest):
    template_name = "admin/livro/dashboard_admin_criar_emprestimo.html"
    url_redirect = "/administrador/livros/"
    if request.method == 'GET':
        formulario = FormularioCriarEmprestimo()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioCriarEmprestimo(request.POST)
        if formulario.is_valid():
            usuario_formulario = formulario.cleaned_data['usuario']
            livro_formulario = formulario.cleaned_data['livro']
            emprestimo_existe = Emprestimo.objects.filter(usuario=usuario_formulario, livro=livro_formulario).exists()
            if not emprestimo_existe:
                # 1. É necessário verificar o tipo de usuário a qual o emprestimo está sendo associado
                # 2. A partir do tipo de usuário, verificar se aquele já tem um numero máximo de emprestimos
                #    para seu tipo de usuário.Como segue abaixo:
                #       i. Alunos podem fazer até 4 emprestimos ao mesmo tempo por até 15 dias cada;
                #       ii. Professores podem fazer até 5 emprestimos ao mesmo tempo por até 30 dias cada;
                #       iii. Funcionários podem fazer até 4 emprestimos ao mesmo tempo por até 21 dias cada;
                # 3. A quantidade de emprestimos de um livro deve obedecer ao numéro máximo de cópias
                #    cadastradas no banco de dados.
                tipo_usuario = retorna_instancia_usuario(usuario=formulario.cleaned_data['usuario'])
                if isinstance(tipo_usuario, Aluno):                    
                    return salvar_emprestimo(request, formulario, 'aluno') # Para Aluno
                elif isinstance(tipo_usuario, Professor):
                    return salvar_emprestimo(request, formulario, 'professor') # Para Professor
                elif isinstance(tipo_usuario, Funcionario):
                    return salvar_emprestimo(request, formulario, 'funcionario') # Para Funcionario
                else:
                    # Levanta uma mensagem de erro, porque o usuário não é nenhum desses três elementos
                    messages.add_message(request, messages.ERROR, 'O usuário não pode alugar um livro')
                    return redirect(url_redirect)
            else:
                messages.add_message(request, messages.ERROR, 'Esse registro já existe no banco de dados.')
                return redirect(url_redirect)
        else:
            messages.add_message(request, messages.ERROR, 'Formulário inválido.')
            return redirect(url_redirect)


def informacoes_emprestimo(request: HttpRequest, eid: int):
    template_name = "admin/livro/dashboard_admin_detalhes_livros.html"
    if request.method=='GET':
        emprestimo=Emprestimo.objects.get(id=eid)
        if emprestimo:
            return render(request, template_name, context={'emprestimo':emprestimo})
        else:
            messages.add_message(request, messages.ERROR, 'Emprestimo não encontrado.')
            return redirect('/administrador/livros/')


def atualizar_informacoes_emprestimo(request: HttpRequest, eid: int):
    # TODO: Resolver bug de atualizar informações de emprestimos:
    # 1. Formulário não carrega as informações do banco;
    template_name = "admin/livro/dashboard_admin_atualizar_emprestimo.html"
    if request.method == 'GET':
        # Resgatar informações da base de dados e mandar para o template
        emprestimo_existe = Emprestimo.objects.filter(id=eid).exists()
        if emprestimo_existe:
            emprestimo = Emprestimo.objects.get(id=eid)
            data = informacoes_formulario_emprestimo(emprestimo)
            formulario = FormularioAtualizarEmprestimo(initial=data)
            return render(request, template_name, context={'form':formulario, 'emprestimo':emprestimo})
        else:
            messages.add_message(request, messages.ERROR, 'Emprestimo solicitado não existe na base de dados.')
            return redirect('/administrador/livros/')
    if request.method == 'POST':
        # Salvar as informações do formulário na base de dados
        formulario = FormularioAtualizarEmprestimo(request.POST)
        if formulario.is_valid():
            emprestimo_existe = Emprestimo.objects.filter(id=eid).exists()
            if emprestimo_existe:
                try:
                    emprestimo = Emprestimo.objects.get(id=eid)
                    emprestimo.usuario = User.objects.get(id=formulario.cleaned_data['usuario'])
                    emprestimo.livro = Livro.objects.get(id=formulario.cleaned_data['livro'])
                    emprestimo.data_emprestimo = formulario.cleaned_data['data_emprestimo']
                    emprestimo.data_devolucao = formulario.cleaned_data['data_devolucao']
                    emprestimo.save()
                    messages.add_message(request, messages.SUCCESS, 'Emprestimo Atualizado com sucesso.')
                    return redirect('/administrador/livros/')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f'Um erro aconteceu ao salvar as informações de emprestimo. {e}.')
                    return redirect('/administrador/livros/')
            else:
                messages.add_message(request, messages.ERROR, 'o Registro não existe  na base de dados.')
                return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Formulário inválido.')
            redirect('/administrador/livros/')


def deletar_emprestimo(request: HttpRequest, eid: int):
    emprestimo_existe = Emprestimo.objects.filter(id=eid).exists()
    url_redirect = "/administrador/livros/"
    if emprestimo_existe:
        emprestimo = Emprestimo.objects.get(id=eid)
        livro = emprestimo.livro    # type: ignore
        livro.copias += 1           # type: ignore
        livro.save()                # type: ignore
        emprestimo.delete()
        messages.add_message(request, messages.SUCCESS, 'Emprestimo apagado com sucesso.')
        return redirect(url_redirect)
    else:
        messages.add_message(request, messages.ERROR, 'Emprestimo não existe na base de dados.')
        return redirect(url_redirect)

# Cursos: dashboard e crud


def dashboard_admin_cursos(request: HttpRequest): # type: ignore
    template_name = 'admin/curso/dashboard_admin_cursos.html'
    if request.method == 'GET':
        cursos = Curso.objects.all()
        contador = {'cursos':len(cursos)}
        paginador_cursos = Paginator(cursos, 20)
        cursos = paginador_cursos.get_page(request.GET.get('page'))
        return render(request, template_name,context={'cursos':cursos, 'contador':contador})


def criar_curso(request: HttpRequest):
    template_name = 'admin/curso/dashboard_admin_criar_curso.html'
    if request.method == 'GET':
        formulario = FormularioCurso()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario=FormularioCurso(request.POST)
        if formulario.is_valid():
            curso = Curso.objects.filter(
                    Q(cod_curso=formulario.cleaned_data['cod_curso']) | 
                    Q(curso=formulario.cleaned_data['curso'])
                ).exists()
            if not curso:
                try:
                    curso = Curso.objects.create(
                        cod_curso=formulario.cleaned_data['cod_curso'],
                        curso=formulario.cleaned_data['curso'],
                        descricao=formulario.cleaned_data['descricao'],
                        turno=formulario.cleaned_data['turno'],
                        duracao=formulario.cleaned_data['duracao'],
                    )
                    messages.add_message(request, messages.SUCCESS, f'O curso {curso.curso} foi criado com sucesso.') # type: ignore
                    return redirect('/administrador/cursos/')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f'Ocorreu um erro ao criar o curso. Erro: {e}')
                    return redirect('/administrador/cursos/')
            else:
                messages.add_message(request, messages.ERROR, 'Um curso com esse nome ou código já existe na base de dados.')
                return render(request, template_name, context={'form':formulario})
        else:
            messages.add_message(request, messages.ERROR, 'Formulário inválido.')
            return redirect('/administrador/cursos/')


def informacoes_curso(request: HttpRequest, cid: int):
    template_name = 'admin/curso/dashboard_admin_detalhes_curso.html'
    if request.method == 'GET':
        curso = Curso.objects.filter(id=cid).exists()
        if curso:
            curso = Curso.objects.get(id=cid) 
            return render(request, template_name, context={'curso':curso})
        else:
            messages.add_message(request, messages.ERROR, 'Curso não encontrado.')
            return redirect('/administrador/cursos/')


def atualizar_informacoes_curso(request: HttpRequest, cid: int):
    template_name = 'admin/curso/dashboard_admin_atualizar_curso.html'
    if request.method=='GET':
        curso = Curso.objects.filter(id=cid).exists()
        if curso:
            curso = Curso.objects.get(id=cid)
            data = informacoes_formulario_curso(curso)
            formulario = FormularioCurso(initial=data)
            return render(request, template_name, context={'form':formulario, 'curso':curso})
        else:
            messages.add_message(request, messages.ERROR, 'Curso não encontrado')
            return redirect('/administrador/cursos/')
    if request.method=='POST':
        formulario = FormularioCurso(request.POST)
        if formulario.is_valid():
            curso = Curso.objects.filter(id=cid).exists()
            if curso:
                try:
                    curso = Curso.objects.get(id=cid)
                    curso.cod_curso = formulario.cleaned_data['cod_curso']
                    curso.curso = formulario.cleaned_data['curso']
                    curso.descricao = formulario.cleaned_data['descricao']
                    curso.duracao = formulario.cleaned_data['turno']
                    curso.duracao = formulario.cleaned_data['duracao']
                    curso.save()
                    messages.add_message(request, messages.SUCCESS, 'Curso atualizado com sucesso.')
                    return redirect('/administrador/cursos/')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f'Erro ao salvar as informações.{e}')
                    return redirect('/administrador/cursos/')
            else:
                messages.add_message(request, messages.ERROR, 'Curso não encontrado.')
                return redirect('/administrador/cursos/')
        else:
            messages.add_message(request, messages.ERROR, 'Formulário Inválido.')
            return redirect('/administrador/cursos/')


def deletar_curso(request: HttpRequest, cid: int):
    if request.method=='GET':
        curso = Curso.objects.filter(id=cid).exists()
        if curso:
            curso = Curso.objects.get(id=cid)
            curso.delete()
            messages.add_message(request, messages.SUCCESS, 'Curso deletado com sucesso.')
            return redirect('/administrador/cursos/')
        else:
            messages.add_message(request, messages.ERROR, 'Curso não encontrado.')
            return redirect('/administrador/cursos/')