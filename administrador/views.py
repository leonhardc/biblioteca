from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from usuario.models import Aluno, Professor, Funcionario
from django.contrib.auth.models import User
from django.contrib import messages
from livro.models import Livro, Autor, Categoria, Reserva, Emprestimo
from usuario.forms import FormularioAluno, FormularioProfessor, FormularioFuncionario
from livro.forms import FormularioLivro, FormularioAutor, FormularioCategoria, FormularioEmprestimo, FormularioReserva
from curso.forms import FormularioCurso
from curso.models import Curso
from utils.utils import *

# Views de administrador

def dashboard_admin(request):
    if request.method == 'GET':
        template_name = 'admin/dashboard-admin.html'
        return render(request, template_name)

# Usuários: dashboard e crud

def dashboard_admin_usuarios(request):
    template_name = 'admin/usuario/dashboard_admin_usuarios.html'
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

# views de Alunos

def criar_aluno(request):
    template_name = "admin/usuario/dashboard_admin_criar_aluno.html"
    if request.method == 'GET':
        formulario = FormularioAluno()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioAluno(request.POST)
        if formulario.is_valid():
            usuario = User.objects.filter(username=formulario.cleaned_data['usuario']).exists()
            if not usuario:
                aluno = Aluno.objects.filter(cpf=formulario.cleaned_data['cpf']).exists()
                if not aluno:
                    # criar novo usuario
                    try:
                        usuario = User.objects.create_user(
                            username = formulario.cleaned_data['usuario'],
                            first_name = formulario.cleaned_data['nome'],
                            last_name =  formulario.cleaned_data['sobrenome'],
                            email = formulario.cleaned_data['email'],
                            password = '1234'
                        )
                        curso = Curso.objects.get(cod_curso=formulario.cleaned_data['curso'])
                        aluno = Aluno.objects.create(
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
                messages.add_message(request, messages.ERROR, 'A base de dados já contem um usuário com esse nome.')
                return render(request, template_name, context={'form':formulario})
        else:
            # Retorna o formulário com mensagem de erro
            messages.add_message(request, messages.ERROR, 'Problemas ao salvar os dados do formulario no banco de dados.')
            return render(request, template_name, context={'form':formulario})

def informacoes_aluno(request, uid):
    if request.method == 'GET':
        template_name = 'admin/usuario/dashboard_admin_detalhes_usuarios.html'
        aluno = Aluno.objects.get(id=uid)
        contexto = {'aluno': aluno}
        return render(request, template_name, context=contexto)

def atualizar_infomacoes_aluno(request, uid):
    """ Em desenvolvimento """
    template_name = "admin/usuario/dashboard_admin_atualizar_aluno.html"
    if request.method == "GET":
        aluno = Aluno.objects.get(id=uid)
        endereco = separar_endereco(aluno.endereco)
        data = informacoes_formulario_aluno(aluno, endereco)
        formulario = FormularioAluno(initial=data)
        return render(request, template_name, context={"form": formulario, 'aluno': aluno})
    if request.method == "POST":
        formulario = FormularioAluno(request.POST)
        if formulario.is_valid():
            aluno = Aluno.objects.filter(id = uid).exists()
            if aluno:
                usuario = User.objects.get(id = uid)
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
                messages.add_message(request, messages.SUCCESS, 'Os dados foram salvos com sucesso.')
                return redirect(f'/administrador/informacoes-aluno/{uid}/')
            else:
                messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
                return redirect(f'/administrador/informacoes-aluno/{uid}/')
        else:
            aluno = Aluno.objects.get(id=uid)
            return render(request, template_name, context={"form": formulario, 'aluno': aluno})

def deletar_aluno(request, uid):
    aluno = Aluno.objects.get(id=uid)
    if aluno:
        aluno.delete()
        messages.add_message(request, messages.SUCCESS, f'Aluno deletado com sucesso.')
        return redirect('/administrador/usuarios/')
    else: 
        messages.add_message(request, messages.ERROR, f'Erro ao deletar o Aluno.')
        return redirect('/administrador/usuarios/')

# views de Professores

def criar_professor(request):
    template_name = "admin/usuario/dashboard_admin_criar_professor.html"
    if request.method == 'GET':
        formulario = FormularioProfessor()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioProfessor(request.POST)
        if formulario.is_valid():
            usuario = User.objects.filter(username=formulario.cleaned_data['usuario']).exists()
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
                messages.add_message(request, messages.ERROR, 'A base de dados já contem um usuário com esse nome.')
                return render(request, template_name, context={'form':formulario})
        else:
            messages.add_message(request, messages.ERROR, 'Problemas ao salvar os dados do formulario no banco de dados.')
            return render(request, template_name, context={'form':formulario})

def informacoes_professor(request, uid):
    if request.method=='GET':
        template_name = 'admin/usuario/dashboard_admin_detalhes_usuarios.html'
        professor = Professor.objects.get(id=uid)
        contexto = {}
        contexto['professor'] = professor
        return render(request, template_name, context=contexto)

def atualizar_informacoes_professor(request, uid):
    """ Em desenvolvimento """
    template_name = "admin/usuario/dashboard_admin_atualizar_professor.html"
    if request.method == 'GET':
        professor = Professor.objects.get(id=uid)
        data = informacoes_formulario_professor(professor)
        formulario = FormularioProfessor(initial=data)
        return render(request, template_name, context={"form": formulario, 'professor':professor})
    if request.method == 'POST':
        formulario = FormularioProfessor(request.POST)
        if formulario.is_valid():
            professor = Professor.objects.get(id=uid)
            if professor:
                usuario = User.objects.get(id = professor.usuario.id)
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
                usuario.save()
                professor.save()
                messages.add_message(request, messages.SUCCESS, 'Os dados foram salvos com sucesso.')
                return redirect(f'/administrador/informacoes-professor/{uid}/')
            else:
                messages.add_message(request, messages.ERROR, 'Professor não encontrado.')
                return redirect(f'/administrador/informacoes-professor/{uid}/')
        else: 
            professor = Professor.objects.get(id=uid)
            return render(request, template_name, context={"form": formulario, 'professor': professor})

def deletar_professor(request, uid):
    professor = Professor.objects.get(id=uid)
    if professor:
        professor.delete()
        messages.add_message(request, messages.SUCCESS, f'Aluno deletado com sucesso.')
        return redirect('/administrador/usuarios/')
    else:
        messages.add_message(request, messages.ERROR, f'Erro ao deletar Professor.')
        return redirect('/administrador/usuarios/')

# views de Funcionarios

def criar_funcionario(request):
    template_name = 'admin/usuario/dashboard_admin_criar_funcionario.html'
    if request.method == 'GET':
        formulario = FormularioFuncionario()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioFuncionario(request.POST)
        if formulario.is_valid():
            usuario = User.objects.filter(username=formulario.cleaned_data['usuario']).exists()
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
                messages.add_message(request, messages.ERROR, 'A base de dados já contem um usuário com esse nome.')
                return render(request, template_name, context={'form':formulario})
        else:
            messages.add_message(request, messages.ERROR, 'Problemas ao salvar os dados do formulario no banco de dados.')
            return render(request, template_name, context={'form':formulario})

def informacoes_funcionario(request, uid):
    if request.method=='GET':
        template_name = 'admin/usuario/dashboard_admin_detalhes_usuarios.html'
        funcionario = Funcionario.objects.get(id=uid)
        contexto = {}
        contexto['funcionario'] = funcionario
        return render(request, template_name, context=contexto)

def atualizar_informacoes_funcionario(request, uid):
    template_name = 'admin/usuario/dashboard_admin_atualizar_funcionario.html'
    if request.method == "GET":
        funcionario = Funcionario.objects.get(id=uid)
        data = informacoes_formulario_funcionario(funcionario)
        formulario = FormularioFuncionario(initial=data)
        return render(request, template_name, context={"form": formulario, 'funcionario':funcionario})
    if request.method == "POST":
        formulario = FormularioFuncionario(request.POST)
        if formulario.is_valid():
            funcionario = Funcionario.objects.get(id=uid)
            if funcionario:
                usuario = User.objects.get(id = funcionario.usuario.id)
                # Salvando os dados do formulário no banco de dados
                usuario.first_name = formulario.cleaned_data['nome']
                usuario.last_name = formulario.cleaned_data['sobrenome']
                usuario.email = formulario.cleaned_data['email']
                usuario.username = formulario.cleaned_data['usuario']
                funcionario.matricula = formulario.cleaned_data['matricula']
                funcionario.cpf = formulario.cleaned_data['cpf']
                usuario.save()
                funcionario.save()
                messages.add_message(request, messages.SUCCESS, 'Os dados foram salvos com sucesso.')
                return redirect(f'/administrador/informacoes-funcionario/{uid}/')
            else:
                messages.add_message(request, messages.ERROR, 'Funcionario não encontrado.')
                return redirect(f'/administrador/informacoes-funcionario/{uid}/')
        else:
            funcionario = Funcionario.objects.get(id=uid)
            return render(request, template_name, context={"form": formulario, 'funcionario': funcionario})

def deletar_funcionario(request, uid):
    funcionario = Funcionario.objects.get(id=uid)
    if funcionario:
        funcionario.delete()
        messages.add_message(request, messages.SUCCESS, f'Aluno deletado com sucesso.')
        return redirect('/administrador/usuarios/')
    else:
        messages.add_message(request, messages.ERROR, f'Erro ao deletar Funcionario.')
        return redirect('/administrador/usuarios/')

# Livros: dashboard e crud

# Views de Livros

def dashboard_admin_livros(request):
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

def criar_livro(request):
    template_name = 'admin/livro/dashboard_admin_criar_livro.html'
    if request.method == 'GET':
        formulario = FormularioLivro()
        return render(request,template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioLivro(request.POST)
        if formulario.is_valid():
            livro = Livro.objects.filter(isbn=formulario.cleaned_data['isbn']).exists()
            if not livro:
                try:
                    livro = Livro(
                        isbn=formulario.cleaned_data['isbn'],
                        titulo=formulario.cleaned_data['titulo'],
                        subtitulo=formulario.cleaned_data['subtitulo'],
                        lancamento=formulario.cleaned_data['lancamento'],
                        editora=formulario.cleaned_data['editora'],
                        copias=formulario.cleaned_data['copias'],
                        categoria=formulario.cleaned_data['categoria'],
                    )
                    livro.save()
                    livro.autores.set(formulario.cleaned_data['autores'])
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

def informacoes_livro(request, lid):
    template_name = 'admin/livro/dashboard_admin_detalhes_livros.html'
    if request.method == 'GET':
        livro = Livro.objects.get(id=lid)
        if livro:
            return render(request, template_name, context={'livro':livro})
        else:
            messages.add_message(request, messages.ERROR, 'Não foi possivel encontra o livro solicitado.')
            return redirect('/administrador/livros/')

def atualizar_informacoes_livro(request, lid):
    template_name = 'admin/livro/dashboard_admin_atualizar_livro.html'
    if request.method=='GET':
        livro = Livro.objects.filter(id=lid).exists()
        if livro:
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
            livro = Livro.objects.filter(id=lid).exists()
            if livro:
                try:
                    livro = Livro.objects.get(id=lid)
                    livro.titulo = formulario.cleaned_data['titulo']
                    livro.subtitulo = formulario.cleaned_data['subtitulo']
                    livro.lancamento = formulario.cleaned_data['lancamento']
                    livro.editora = formulario.cleaned_data['editora']
                    livro.copias = formulario.cleaned_data['copias']
                    livro.autores.set(formulario.cleaned_data['autores'])
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

def deletar_livro(request, lid):
    if request.method=='GET':
        livro = Livro.objects.get(id=lid)
        if livro:
            livro.delete()
            messages.add_message(request, messages.INFO, 'Livro deletado com sucesso.')
            return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.INFO, 'Livro não encontrado.')
            return redirect('/administrador/livros/')

## Views de Autores

def criar_autor(request):
    template_name = 'admin/livro/dashboard_admin_criar_autor.html'
    if request.method == 'GET':
        formulario = FormularioAutor()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioAutor(request.POST)
        if formulario.is_valid():
            autor = Autor.objects.filter(cpf=formulario.cleaned_data['cpf']).exists()
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

def informacoes_autor(request, aid):
    template_name = 'admin/livro/dashboard_admin_detalhes_livros.html'
    if request.method=='GET':
        autor = Autor.objects.get(id=aid)
        if autor:
            return render(request, template_name, context={'autor':autor})
        else:
            messages.add_message(request, messages.ERROR, 'Autor não encontrado.')
            return redirect('/administrador/livros/')

def atualizar_informacoes_autor(request, aid):
    template_name = 'admin/livro/dashboard_admin_atualizar_autor.html'
    if request.method == 'GET':
        autor = Autor.objects.get(id=aid)
        data = informacoes_formulario_autor(autor)
        formulario = FormularioAutor(initial=data)
        return render(request, template_name, context={'form':formulario, 'autor':autor})
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

def deletar_autor(request, aid):
    if request.method == 'GET':
        autor = Autor.objects.get(id=aid)
        if autor:
            autor.delete()
            messages.add_message(request, messages.INFO, 'Autor deletado com sucesso.')
            return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Autor não encontrado.')
            return redirect('/administrador/livros/')

## Views de Categorias

def criar_categoria(request):
    template_name = 'admin/livro/dashboard_admin_criar_categoria.html'
    if request.method == 'GET':
        formulario = FormularioCategoria()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario = FormularioCategoria(request.POST)
        if formulario.is_valid():
            categoria = Categoria.objects.filter(categoria=categoria).exists()
            if not categoria:
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

def informacoes_categoria(request, cid):
    template_name = 'admin/livro/dashboard_admin_detalhes_livros.html'
    if request.method=='GET':
        categoria = Categoria.objects.get(id=cid)
        if categoria:
            return render(request, template_name, context={'categoria':categoria})
        else:
            messages.add_message(request, messages.ERROR, 'Categoria não encontrada')
            return redirect('/administrador/livros/')

def atualizar_informacoes_categoria(request, cid):
    template_name = 'admin/livro/dashboard_admin_atualizar_categoria.html'
    if request.method=='GET':
        categoria = Categoria.objects.get(id=cid)
        data = informacoes_formulario_categoria(categoria)
        formulario = FormularioCategoria(initial=data)
        return render(request, template_name, context={'form': formulario, 'categoria': categoria})
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

def deletar_categoria(request, cid):
    if request.method == 'GET':
        categoria = Categoria.objects.get(id=cid)
        if categoria:
            categoria.delete()
            messages.add_message(request, messages.INFO, 'Categoria deletada com sucesso.')
            return redirect('/administrador/livros/')
        else:
            messages.add_message(request, messages.ERROR, 'Categoria não encontrada.')
            return redirect('/administrador/livros/')

## Views de Reservas

def criar_reserva(request):
    pass

def informacoes_reserva(request, rid):
    template_name = 'admin/livro/dashboard_admin_detalhes_livros.html'
    if request.method=='GET':
        reserva=Reserva.objects.get(id=rid)
        if reserva:
            return render(request, template_name, context={'reserva':reserva})
        else:
            messages.add_message(request, messages.ERROR, 'Reserva não encontrada.')
            return redirect('/administrador/livros/')

def atualizar_informacoes_reserva(request, rid):
    pass

def deletar_reserva(request, rid):
    pass

## Views de Emprestimos

def criar_emprestimo(request):
    pass

def informacoes_emprestimo(request, eid):
    template_name = 'admin/livro/dashboard_admin_detalhes_livros.html'
    if request.method=='GET':
        emprestimo=Emprestimo.objects.get(id=eid)
        if emprestimo:
            return render(request, template_name, context={'emprestimo':emprestimo})
        else:
            messages.add_message(request, messages.ERROR, 'Emprestimo não encontrado.')
            return redirect('/administrador/livros/')

def atualizar_informacoes_emprestimo(request, eid):
    pass

def deletar_emprestimo(request, eid):
    pass

# Cursos: dashboard e crud

def dashboard_admin_cursos(request):
    template_name = 'admin/curso/dashboard_admin_cursos.html'
    if request.method == 'GET':
        cursos = Curso.objects.all()
        contador = {'cursos':len(cursos)}
        paginador_cursos = Paginator(cursos, 20)
        cursos = paginador_cursos.get_page(request.GET.get('page'))
        return render(request, template_name,context={'cursos':cursos, 'contador':contador})

def criar_curso(request):
    template_name = 'admin/curso/dashboard_admin_criar_curso.html'
    if request.method == 'GET':
        formulario = FormularioCurso()
        return render(request, template_name, context={'form':formulario})
    if request.method == 'POST':
        formulario=FormularioCurso(request.POST)
        if formulario.is_valid():
            curso = Curso.objects.filter(
                    Q(cod_curso=formulario.cleaned_data['cod_curso']) | Q(curso=formulario.cleaned_data['curso'])
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
                    messages.add_message(request, messages.SUCCESS, f'O curso {curso.curso} foi criado com sucesso.')
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

def informacoes_curso(request, cid):
    template_name = 'admin/curso/dashboard_admin_detalhes_curso.html'
    if request.method == 'GET':
        curso = Curso.objects.get(id=cid)
        if curso:
            return render(request, template_name, context={'curso':curso})
        else:
            messages.add_message(request, messages.ERROR, 'Curso não encontrado.')
            return redirect('/administrador/cursos/')

def atualizar_informacoes_curso(request, cid):
    template_name = 'admin/curso/dashboard_admin_atualizar_curso.html'
    if request.method=='GET':
        curso = Curso.objects.get(id=cid)
        if curso:
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

def deletar_curso(request, cid):
    if request.method=='GET':
        curso = Curso.objects.get(id=cid)
        if curso:
            curso.delete()
            messages.add_message(request, messages.SUCCESS, 'Curso deletado com sucesso.')
            return redirect('/administrador/cursos/')
        else:
            messages.add_message(request, messages.ERROR, 'Curso não encontrado.')
            return redirect('/administrador/cursos/')