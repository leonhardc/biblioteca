from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required
from .models import Livro
from datetime import date
from utils.utils import *
from django.db.models import Q
from usuario.constants import MAX_RESERVAS_POR_USUARIO

# Método de Listar Livros, Autores e Categorias
def listar_livros(request: HttpRequest) -> HttpResponse:
    template_name = "livro/livros.html"
    itens_por_pagina = 20
    termo_pesquisa = request.GET.get("pesquisa", "")
    if termo_pesquisa:
        pesquisa = Livro.objects.filter(
            Q(titulo__icontains=termo_pesquisa)|
            Q(subtitulo__icontains=termo_pesquisa)|
            Q(autores__nome__icontains=termo_pesquisa)).distinct()
        if len(pesquisa) < itens_por_pagina:
            itens_por_pagina = len(pesquisa)
            if itens_por_pagina == 0:
                itens_por_pagina = 1
        page_number = request.GET.get("page")
        paginator = Paginator(pesquisa, itens_por_pagina)
        livros = paginator.get_page(page_number)
        return render(request, template_name=template_name, context={"livros": livros, 'termo_busca': termo_pesquisa})
    else:
        livros = Livro.objects.all()
        paginator = Paginator(livros, itens_por_pagina)
        page_number = request.GET.get("page")
        livros = paginator.get_page(page_number)
        return render(request, template_name=template_name, context={"livros": livros})

def listar_autores(resquest: HttpRequest) -> HttpResponse:
    return HttpResponse('View listar autores')

def listar_categorias(request: HttpRequest) -> HttpResponse:
    return HttpResponse("View listar Categorias")

# Implementação do CRUD para livro
def criar_livro(request: HttpRequest) -> HttpResponse:
    return HttpResponse("View Criar Livro")

def detalhar_livro(request: HttpRequest, id_livro:int) -> HttpResponse:
    livro = Livro.objects.filter(id=id_livro).exists()
    if livro:
        livro = Livro.objects.get(id=id_livro)
        template_name = "livro/detalhar_livro.html"
        return render(request, template_name, context={'livro':livro})
    else:
        # TODO: IMPLEMENTAR LOGICA PARA MANDAR UMA MENSAGEM DE ERRO PARA O TEMPLATE ORIGINAL
        return HttpResponse('Livro não encontrado.')

def atualizar_livro(request:HttpRequest, id_livro:int) -> HttpResponse:
    return HttpResponse("View Atualizar Livro")

def deletar_livro(request:HttpRequest, id_livro:int) -> HttpResponse:
    return HttpResponse("View Deletar Livro")

# Implementação de Emprestimo e Reserva de Livros
def reservar_livro(request:HttpRequest, id_livro:int, usuario:str) -> HttpResponse:
    return HttpResponse("View reservar livro")

def emprestar_livro(request:HttpResponse, id_livro:int, usuario:str) -> HttpResponse:
    return HttpResponse("View Emprestar Livro")

# CRUD para Autor
def criar_autor(request:HttpRequest) -> HttpResponse:
    return HttpResponse("View criar Autor")

def detalhar_autor(request:HttpRequest, id_autor:int) -> HttpResponse:
    return HttpResponse("View detalhar Autor")

def atualizar_autor(request:HttpRequest, id_autor:int) -> HttpResponse:
    return HttpResponse("View atualizar Autor")

def deletar_autor(request:HttpRequest, id_autor:int) -> HttpResponse:
    return HttpResponse("View deletar Autor")

# CRUD para Categoria
def criar_categoria(request:HttpRequest) -> HttpResponse:
    return HttpResponse("View criar Categoria")

def detalhar_categoria(request:HttpRequest, id_categoria:int) -> HttpResponse:
    return HttpResponse("View detalhar Categoria")

def atualizar_categoria(request:HttpRequest, id_categoria:int) -> HttpResponse:
    return HttpResponse("View atualizar Categoria")

def deletar_categoria(request:HttpRequest, id_categoria:int) -> HttpResponse:
    return HttpResponse("View deletar Categoria")

# Funcoes auxiliares para reservas de aluno, professor e funcionario
# TODO: Mover as funcoes auxiliares para utils.py
def reserva_existe(usuario, livro:Livro) -> bool:
    return Reserva.objects.filter(usuario=usuario, livro=livro, ativo=True).exists()

def emprestimo_existe(usuario, livro:Livro) -> bool:
    return Emprestimo.objects.filter(usuario=usuario, livro=livro, ativo=True).exists()

def retorna_pagina_anterior_com_erro(request:HttpRequest, mensagem_erro:str):
    messages.add_message(request, messages.ERROR, mensagem_erro)
    pagina_anterior = request.META.get('HTTP_REFERER')
    return redirect(pagina_anterior)

def cria_nova_reserva(request:HttpRequest, livro:Livro):
    Reserva.objects.create(
        usuario=request.user,
        livro=livro,
        data_reserva=date.today(), 
        ativo=True
    )
    messages.add_message(request, messages.SUCCESS, 'Reserva realizada com sucesso.')
    return redirect('livro:listar_reservas')

def criar_reserva_aluno(request:HttpRequest, id_livro:int):
    aluno = Aluno.objects.get(usuario=request.user)
    if aluno.reservas < MAX_RESERVAS_POR_USUARIO['aluno']:
        livro = Livro.objects.get(id=id_livro) # type: ignore
        if reserva_existe(request.user, livro):
            retorna_pagina_anterior_com_erro(request, 'Reserva já existente para este livro.')
        if emprestimo_existe(request.user, livro):
            retorna_pagina_anterior_com_erro(request, 'Empréstimo já existente para este livro.')
        # Se a reserva ou o emprestimo nao existir, cria uma nova reserva
        cria_nova_reserva(request, livro)
    else:
        retorna_pagina_anterior_com_erro(request, 'Nao eh possivel fazer mais reservas. Usuário já atingiu o numero máximo de reservas.')

def criar_reserva_professor(request:HttpRequest, id_livro:int):
    professor = Professor.objects.get(usuario=request.user)
    if professor.reservas < MAX_RESERVAS_POR_USUARIO['professor']:
        livro = Livro.objects.get(id=id_livro) # type: ignore
        if reserva_existe(request.user, livro):
            retorna_pagina_anterior_com_erro(request, 'Reserva já existente para este livro.')
        if emprestimo_existe(request.user, livro):
            retorna_pagina_anterior_com_erro(request, 'Empréstimo já existente para este livro.')
        # Se a reserva ou o emprestimo nao existir, cria uma nova reserva
        cria_nova_reserva(request, livro)
    else:
        retorna_pagina_anterior_com_erro(request, 'Nao eh possivel fazer mais reservas. Usuário já atingiu o numero máximo de reservas.')

def criar_reserva_funcionario(request:HttpRequest, id_livro:int):
    funcionario = Funcionario.objects.get(usuario=request.user)
    if funcionario.reservas < MAX_RESERVAS_POR_USUARIO['funcionario']:
        livro = Livro.objects.get(id=id_livro) # type: ignore
        if reserva_existe(request.user, livro):
            retorna_pagina_anterior_com_erro(request, 'Reserva já existente para este livro.')
        if emprestimo_existe(request.user, livro):
            retorna_pagina_anterior_com_erro(request, 'Empréstimo já existente para este livro.')
        # Se a reserva ou o emprestimo nao existir, cria uma nova reserva
        cria_nova_reserva(request, livro)
    else:
        retorna_pagina_anterior_com_erro(request, 'Nao eh possivel fazer mais reservas. Usuário já atingiu o numero máximo de reservas.')

# Views de Reserva
def criar_reserva(request: HttpRequest, id_livro:int):
    if request.user.is_authenticated:
        if user_is_aluno(request.user):
            criar_reserva_aluno(request, id_livro)
        elif user_is_professor(request.user):
            criar_reserva_professor(request, id_livro)
        elif user_is_funcionario(request.user):
            criar_reserva_funcionario(request, id_livro)
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:login')

def listar_reservas(request:HttpRequest):
    reservas = Reserva.objects.filter(usuario=request.user).exists()
    template_name = "livro/listar_reservas.html"
    if reservas:
        reservas = Reserva.objects.filter(usuario=request.user)
        return render(request, template_name=template_name, context={'reservas':reservas})
    else:
        messages.add_message(request, messages.ERROR, 'Não existem reservas para este usuário.')
        return render(request, template_name, context={'reserva':True})

def ler_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    reserva = Reserva.objects.filter(id=id_reserva).exists()
    if reserva:
        # TODO: Logica implementada, falta criar o template
        template_name = ""
        reserva = Reserva.objects.get(id=id_reserva)
        return render(request, template_name=template_name, context={})
    else:
        return HttpResponse("Reserva não encontrada.")

def atualizar_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    # Nao deve ser usada ja que a logica de cada reserva impossibilita que os 
    # dados sejam alterados
    return HttpResponse('View de atualizar reserva')

def deletar_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    reserva = Reserva.objects.filter(id=id_reserva).exists()
    if reserva:
        reserva = Reserva.objects.get(id=id_reserva)
        reserva.delete()
        messages.add_message(request, messages.SUCCESS, 'Reserva deletada com sucesso.')
        pagina_anterior = request.META.get('HTTP_REFERER')
        return redirect(pagina_anterior)
    else:
        messages.add_message(request, messages.ERROR, 'Reserva não encontrada.')
        pagina_anterior = request.META.get('HTTP_REFERER')
        return redirect(pagina_anterior)

# Views de Emprestimo

def criar_emprestimo(request: HttpRequest, id_livro:int, id_usuario:int):
    usuario = request.user  # O usuário deve ser um funcionario. Ele pode emprestar livros 
                            # para outros funcionarios, para si mesmo e para alunos e professores
    if usuario.is_authenticated and user_is_funcionario(usuario):
        # O proximo passo é identificar se o usuario que quer fazer o emprestimo eh
        # professor, aluno ou outro funcionario
        pass


def listar_emprestimos(request: HttpRequest):
    if request.user.is_authenticated:
        emprestimos_existem = Emprestimo.objects.filter(usuario=request.user, ativo=True).exists()
        template_name = 'livro/listar_emprestimos.html'
        if emprestimos_existem:
            emprestimos = Emprestimo.objects.filter(usuario=request.user, ativo=True)
            return render(request, template_name, context={'emprestimos': emprestimos})
        else:
            messages.add_message(request, messages.ERROR, 'Não existem emprestimos para este usuário.')
            return render(request, template_name, context={'emprestimo':True})
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        url_anterior = request.META.get('HTTP_REFERER')
        return redirect(url_anterior)

def ler_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('Views de ler emprestimo')

def atualizar_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('View de atualizar emprestimo')

def deletar_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('View de deletar emprestimo')