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
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuario.models import Aluno, Professor, Funcionario
from curso.models import Curso
from utils.utils import *
from utils.formularios.utils_forms import informacoes_formulario_aluno
from django.core.paginator import Paginator
from utils.usuarios.utils import user_is_aluno, user_is_professor, user_is_funcionario
from .constants import *
import datetime
from utils.utils import gerar_matricula_aluno, gerar_matricula_professor, gerar_matricula_funcionario

# Views de controle de usuario
def index(request:HttpRequest) -> HttpResponse:
    # if request.user.is_authenticated:
    template = 'usuario/index.html'
    context_info = {
        'num_livros': len(Livro.objects.all()),
        'num_usuarios': len(User.objects.all()),
    }
    return render(
        request,
        template,
        context={
            'user':request.user,
            "info":context_info
            
        }
    )
    # messages.add_message(request, messages.ERROR, "Operação inválida. O Usuário não está logado.")
    # url_anterior = request.META.get('HTTP_REFERER')
    # return redirect(url_anterior) # type: ignore

def entrar(request:HttpRequest):
    template = 'usuario/entrar.html'
    if request.method == 'GET':
        formulario = LoginForm()
        return render(
            request, 
            template_name=template, 
            context={'form':formulario}
            )


def get_reservas_ativas_usuario(usuario:User):
    return Reserva.objects.filter(usuario=usuario, ativo=True)

def get_emprestimos_ativos_usuario(usuario:User):
    return Emprestimo.objects.filter(usuario=usuario, ativo=True)

def get_emprestimos_pendentes_usuario(usuario:User):
    return Emprestimo.objects.filter(usuario=usuario, ativo=True, pendente=True)

def calcula_emprestimos_pendentes_de_usuario(usuario_id):
    emprestimos = Emprestimo.objects.filter(usuario__id=usuario_id, ativo=True)
    for emprestimo in emprestimos:
        if emprestimo.data_devolucao < datetime.date.today():
            emprestimo.pendente = True
            emprestimo.save()

def pagina_inicial_aluno(request:HttpRequest, uid:int):
    if request.user.is_authenticated:
        template_name='usuario/aluno/dashboard_aluno.html'
        usuario = User.objects.get(id=uid)
        cont_emprestimos = len(get_emprestimos_ativos_usuario(usuario))
        cont_reservas = len(get_reservas_ativas_usuario(usuario))
        cont_emprestimos_pendentes = len(get_emprestimos_pendentes_usuario(usuario))
        # messages.add_message(request, messages.SUCCESS, f'{usuario.username} logado com sucesso!')
        return render(request, template_name=template_name, context={'aluno':{'emprestimos':cont_emprestimos, 'reservas':cont_reservas, 'emprestimos_pendentes':cont_emprestimos_pendentes}})
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

def pagina_inicial_professor(request:HttpRequest, uid:int):
    if request.user.is_authenticated:
        template_name='usuario/professor/dashboard_professor.html'
        usuario = User.objects.get(id=uid)
        messages.add_message(request, messages.SUCCESS, f'{usuario.username} logado com sucesso!')
        return render(request, template_name=template_name)
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

def pagina_inicial_funcionario(request:HttpRequest, uid:int):
    if request.user.is_authenticated:
        template_name='usuario/funcionario/dashboard_funcionario.html'
        usuario = User.objects.get(id=uid)
        messages.add_message(request, messages.SUCCESS, f'{usuario.username} logado com sucesso!')
        return render(request, template_name=template_name)
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

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
            # Operacoes feitas logo apos o login
            login(request, usuario)
            calcula_emprestimos_pendentes_de_usuario(usuario.id)
            if user_is_aluno(usuario):
                return redirect('usuario:pagina_inicial_aluno', uid=usuario.id)
            elif user_is_professor(usuario):
                return redirect('usuario:pagina_inicial_professor', uid=usuario.id)
            elif user_is_funcionario(usuario):
                return redirect('usuario:pagina_inicial_funcionario', uid=usuario.id)
            else: 
                messages.add_message(request, messages.INFO, 'Usuario ou senhas inválidos')
                return redirect('usuario:entrar')
        else:
            messages.add_message(request, messages.INFO, 'Formulário inválido')
            return redirect('usuario:entrar')

def sair(request:HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return redirect('usuario:entrar')
    messages.add_message(request, messages.ERROR, 'Operacao inválida. Usuário não autenticado')
    return redirect('usuario:entrar')


# CRUD de Aluno
def listar_alunos(request:HttpRequest):
    if request.user.is_authenticated:
        template_name = 'usuario/aluno/listar_alunos.html'
        lista_de_alunos = Aluno.objects.all()
        paginator = Paginator(lista_de_alunos, 20)  
        numero_da_pagina = request.GET.get("page")
        alunos = paginator.get_page(numero_da_pagina)
        return render(  
            request, 
            template_name, 
            context={
                'alunos':alunos
                }
            )
    messages.add_message(
        request,
        messages.ERROR,
        "O usuario não está autenticado"
    )
    url_anterior = request.META.get('HTTP_REFERER')
    return redirect(url_anterior) # type: ignore

def dashaboard_aluno(request:HttpRequest):
    if request.method == "GET" and request.user.is_authenticated:
        template_name = "usuario/aluno/dashboard_aluno.html"
        contexto = {
            'dashboard': True,
        }
        return render(request, template_name, context=contexto)
    messages.add_message(
        request,
        messages.ERROR,
        'Operação inválida. O usuário não está logado.'
    )
    url_anterior = request.META.get('HTTP_REFERER')
    return redirect(url_anterior) # type: ignore

def criar_aluno(request:HttpRequest):
    if request.user.is_authenticated:
        if request.method == 'GET':
            formulario_aluno = FormularioAluno()
            template_name = 'formulario-cadastro-aluno.html'
            return render(request, template_name, context={'form':formulario_aluno})
        if request.method == 'POST':
            formulario = FormularioAluno(request.POST)
            # Dados de Usuario
            nome = formulario.cleaned_data['nome']
            sobrenome = formulario.cleaned_data['sobrenome']
            email = formulario.cleaned_data['email']
            usuario = formulario.cleaned_data['usuario']
            cpf = formulario.cleaned_data['cpf']
            # Dados de endereco
            endereco_formatado = formatar_endereco(formulario)
            # Dados de curso
            matricula = formulario.cleaned_data['matricula']
            curso = Curso.objects.get(id=formulario.cleaned_data['curso'])
            ingresso = formulario.cleaned_data['ingresso']
            conclusao_prevista = formulario.cleaned_data['conclusao_prevista']
            # Passo 1: Criar o Usuario
            # 1.1 - Checar se o usuario ja existe, se sim dar mensagem de erro
            usuario_existe = User.objects.filter(username=usuario).exists()
            if usuario_existe:
                messages.add_message(request, messages.ERROR, 'Erro ao adicionar novo usuario. O username ja existe na base de dados.')
                url_anterior = request.META.get('HTTP_REFERER')
                return redirect(url_anterior) # type: ignore
            # 1.2 - Criar Usuario com nome, sobrenome, username, e senha padrao 1234
            else:
                novo_usuario = User.objects.create_user(
                    username=usuario,
                    email=email,
                    password='1234',
                    first_name = nome,
                    last_name=sobrenome
                )
            # Passo 2: Criar o Aluno
            # 2.1 Criar Matricula e verificar se a matricula ja existe, sair do loop so quando a matricula ja estiver criada
            matricula = ''
            while True:
                matricula = f'{random.randint(100000, 999999)}'
                if not Aluno.objects.filter(matricula=matricula).exists():
                    break        
            # 2.2 Criar o Aluno na base de dados
            novo_aluno = { # type: ignore
                'usuario':novo_usuario,
                'matricula':matricula,
                'curso': curso,
                'endereco': endereco_formatado,
                'cpf': cpf,
                'ingresso': ingresso,
                'conclusao_prevista': conclusao_prevista,
                'ativo': True,
                'reservas': 0,
                'reservas': 0,
            }
            Aluno.objects.create(**novo_aluno)
            messages.add_message(request, messages.SUCCESS, 'Aluno adicionado com sucesso.')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior) # type: ignore
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'Operação inválida. O usuário não está logado.'
        )
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

def ler_aluno_administrador(request:HttpRequest, uid:int):
    # TODO: Criar o template abaixo
    if request.user.is_authenticated:
        if request.user.is_staff or user_is_funcionario(request.user):
            template_name = "usuario/aluno/ler_aluno.html"
            if Aluno.objects.filter(id=uid).exists():
                aluno = Aluno.objects.get(id=uid)
                return render(request, template_name, context={'aluno':aluno})
            else: 
                url_anterior = request.META.get('HTTP_REFERER')
                messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
                return redirect(url_anterior) # type: ignore
        messages.add_message(
            request,
            messages.ERROR,
            'Operação inválida. O usuário logado não tem permissão para fazer esta operação.'
        )   
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior)     # type: ignore
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'Operação inválida. O usuário não está logado, ou não tem permissões de administrador.'
        )
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

def ler_aluno(request:HttpRequest):
    if request.user.is_authenticated:
        if request.method == 'GET':
            template_name = 'usuario/aluno/ler_aluno.html'
            aluno = Aluno.objects.get(usuario=request.user)
            return render(request, template_name, context={'aluno':aluno, 'conta': True})
        else:
            messages.add_message(request, messages.ERROR, OPERACAO_INVALIDA)
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior) # type: ignore

    else:
        messages.add_message(request, messages.ERROR, USUARIO_NAO_AUTENTICADO)
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

def atualizar_aluno(request:HttpRequest, uid:int):
    # TODO: Essa view so pode ser acessada por funcionarios, administradores e pelo aluno
    # TODO: Criar o template abaixo
    if request.user.is_authenticated:
        template_name = 'usuario/aluno/atualizar_dados_aluno.html'
        if request.user.is_staff or user_is_funcionario(request.user):
            if request.method == 'GET':
                if Aluno.objects.filter(id=uid).exists():
                    aluno = Aluno.objects.get(id=uid)
                    endereco = separar_endereco(aluno.endereco) 
                    data_aluno = informacoes_formulario_aluno(aluno, endereco)
                    formulario = FormularioAluno(initial=data_aluno)
                    return render(request, template_name, context={'aluno':aluno, 'form':formulario})
                else:
                    messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
                    url_anterior = request.META.get('HTTP_REFERER')
                    return redirect(url_anterior) # type: ignore
            if request.method == 'POST':
                formulario = FormularioAluno(request.POST)
                aluno = Aluno.objects.get(usuario=formulario.cleaned_data['usuario'])
                # Dados de Usuario
                aluno.usuario = formulario.cleaned_data['usuario']
                aluno.nome = formulario.cleaned_data['nome'] # type: ignore
                aluno.sobrenome = formulario.cleaned_data['sobrenome'] # type: ignore
                aluno.email = formulario.cleaned_data['email'] # type: ignore
                aluno.cpf = formulario.cleaned_data['cpf']
                # Dados de endereco
                aluno.endereco_formatado = formatar_endereco(formulario) # type: ignore
                # Dados de curso
                aluno.matricula = formulario.cleaned_data['matricula']
                aluno.curso = Curso.objects.get(id=formulario.cleaned_data['curso'])
                aluno.ingresso = formulario.cleaned_data['ingresso']
                aluno.conclusao_prevista = formulario.cleaned_data['conclusao_prevista']
                aluno.save()
                messages.add_message(request,messages.SUCCESS,'Os dados do aluno foram salvos com sucesso.')
                url_anterior = request.META.get('HTTP_REFERER')
                return redirect(url_anterior) # type: ignore
        else:
            messages.add_message(request,messages.ERROR,'Operação inválida. O usuário nao é administrador ou funcionario.')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior) # type: ignore
    else:
        messages.add_message(request,messages.ERROR,'Operação inválida. O usuário nao esta autenticado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

def deletar_aluno(request:HttpRequest, uid:int):
    # TODO: Somente acessivel pelo usuario administrador
    if Aluno.objects.filter(id=uid).exists() and request.user.is_authenticated:
        Aluno.objects.get(id=uid).delete()
        return HttpResponse("Aluno Deletado com Sucesso.")
    else: 
        url_anterior = request.META.get('HTTP_REFERER')
        messages.add_message(request, messages.ERROR, 'Aluno não encontrado')
        return redirect(url_anterior) # type: ignore

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
            return redirect(url_anterior) # type: ignore
    else:
        url_anterior = request.META.get('HTTP_REFERER')
        messages.add_message(request, messages.ERROR, 'Usuario não autenticado')
        return redirect(url_anterior) # type: ignore


# CRUD de Professor
def criar_professor(request:HttpRequest):
    if request.user.is_authenticated:
        if request.method == 'GET':
            template_name = 'usuario/professor/criar_professor.html'
            formulario_professor = FormularioProfessor()
            return render(request, template_name, context={'form': formulario_professor})
        if request.method == 'POST':
            formulario = FormularioProfessor(request.POST)
            nome = formulario.cleaned_data['nome']
            sobrenome = formulario.cleaned_data['sobrenome']
            email = formulario.cleaned_data['email']
            usuario = formulario.cleaned_data['usuario']
            cpf = formulario.cleaned_data['cpf']
            # matricula = formulario.cleaned_data['matricula']
            curso = Curso.objects.get(id=formulario.cleaned_data['curso'])
            regime = formulario.cleaned_data['regime']
            contratacao = formulario.cleaned_data['contratacao']
            # Passo 1: Criar o Usuario
            # 1.1 - Checar se o usuario ja existe, se sim dar mensagem de erro
            usuario_existe = User.objects.filter(username=usuario).exists()
            if usuario_existe:
                messages.add_message(request, messages.ERROR, 'Erro ao adicionar novo usuario. O username ja existe na base de dados.')
                url_anterior = request.META.get('HTTP_REFERER')
                return redirect(url_anterior) # type: ignore
            # 1.2 - Criar Usuario com nome, sobrenome, username, e senha padrao 1234
            try:
                novo_usuario = User.objects.create_user(
                    username=usuario,
                    email=email,
                    password='1234',
                    first_name = nome,
                    last_name=sobrenome
                )
            except Exception as e:
                messages.add_message(request, messages.ERROR, f'Erro ao criar novo usuario. {e}')
                url_anterior = request.META.get('HTTP_REFERER')
                return redirect(url_anterior) # type: ignore
            # Passo 2: Criar o Professor
            # 2.1 Criar Matricula e verificar se a matricula ja existe, sair do loop so quando a matricula ja estiver criada
            matricula = gerar_matricula_professor()
            novo_professor = {
                'usuario':novo_usuario,
                'matricula':matricula,
                'curso': curso,
                'cpf': cpf,
                'regime': regime,
                'contratacao': contratacao,
                'ativo': True,
            }
            try:
                Professor.objects.create(**novo_professor)
            except Exception as e:
                messages.add_message(request, messages.ERROR, f'Erro ao criar novo professor. {e}')
                url_anterior = request.META.get('HTTP_REFERER') 
            messages.add_message(request, messages.SUCCESS, 'Professor adicionado com sucesso.')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior) # type: ignore
    else:
        messages.add_message(request, messages.ERROR, 'O usuário não está autenticado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

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
            return redirect(url_anterior) # pyright: ignore[reportArgumentType]
    else:
        messages.add_message(request, messages.ERROR, 'O usuário nao esta logado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

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
            return redirect(url_anterior) # type: ignore
        else: 
            messages.add_message(request, messages.ERROR, 'O usuario solicitado não existe na base de dados.')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior) # type: ignore
    else:
        messages.add_message(request, messages.ERROR, 'O usuario nao esta autenticado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

def detalhes_professor(request:HttpRequest, uid:int):
    if request.method=='GET':
        template_name = 'admin/dashboard_admin_detalhes_usuarios.html'
        professor = Professor.objects.get(id=uid)
        contexto = {}
        contexto['professor'] = professor
        return render(request, template_name, context=contexto) # type: ignore

def listar_todas_as_reservas(request:HttpRequest):
    pass

# CRUD de Funcionário
def criar_funcionario(request:HttpRequest):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # TODO: Implementar o template abaixo
            template_name = 'ususario/funcionario/criar_funcionario.html'
            formulario_funcionario = FormularioFuncionario()
            return render(request, template_name, context={'form':formulario_funcionario})
        if request.method == 'POST':
            # TODO: Implementar a regra de criar funcionario
            pass
    else:
        messages.add_message(request, messages.ERROR, 'O usuario nao esta autenticado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

def ler_funcionario(request:HttpRequest, uid:int):
    if request.user.is_authenticated:
        template_name = 'usuario/funcionario/detales_funcionario.html'
        funcionario_existe = Funcionario.objects.filter(id=uid).exists()
        if funcionario_existe:
            funcionario = Funcionario.objects.get(id=uid)
            return render(request, template_name, context={'funcionario':funcionario})
        else:
            messages.add_message(request, messages.ERROR, 'O usuário buscado nao existe na base de dados.')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior) # type: ignore
    else:
        messages.add_message(request, messages.ERROR, 'O usuario nao esta autenticado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

def atualizar_funcionario(request:HttpRequest, uid:int):
    if request.user.is_authenticated:
        template_name = 'usuario/funcionario/atualizar_funcionario.html'
        if request.method == 'GET':
            # TODO: Adicionar dados iniciais no formulario
            formulario_funcionario = FormularioFuncionario()
            return render(request, template_name, context={'form':formulario_funcionario})
        if request.method == 'POST':
            # TODO: Salvar os dados no banco de dados
            pass
    else:
        messages.add_message(request, messages.ERROR, 'O usuario nao esta autenticado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

def deletar_funcionario(request:HttpRequest, uid:int):
    if request.user.is_authenticated:
        funcionario_existe = Funcionario.objects.filter(id=uid).exists()
        if funcionario_existe:
            funcionario = Funcionario.objects.get(id=uid)
            funcionario.delete()
            messages.add_message(request, messages.SUCCESS, 'Funcionario deletado com sucesso.')
            url_anterior = request.META.get('HTTP_REFERER')
            return redirect(url_anterior) # type: ignore
    else:
        messages.add_message(request, messages.ERROR, 'O usuario nao esta autenticado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior) # type: ignore

def detalhes_funcionario(request:HttpRequest, uid:int):
    if request.method=='GET':
        template_name = 'admin/dashboard_admin_detalhes_usuarios.html'
        funcionario = Funcionario.objects.get(id=uid)
        return render(request, template_name, context={'funcionario':funcionario})
