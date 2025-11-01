from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from .models import Livro
from datetime import date
from utils.utils import *
from django.db.models import Q

MAX_RESERVAS_POR_USUARIO = (
    ('aluno', 10),
    ('professor', 10),
    ('funcionario', 10),
)
MAX_EMPRESTIMOS_POR_USUARIO = (
    ('aluno', 10),
    ('professor', 10),
    ('funcionario', 10),
)
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

# Views de Reserva
def criar_reserva(request: HttpRequest, id_livro:int):
    if request.user.is_authenticated:
        # 1. verificar se o usuario eh aluno professor ou funcionario
            # i. Aluno Professor e Funcionario podem ambos fazer no maximo 10 reservas.
        # 2. checar se eh possivel aquele usuario fazer mais alguma reserva
        # 3. se sim, fazer a reserva para o usuario e redirecionar para o template de livros
        # 4. se nao, retornar uma mensagem de erro
        # TODO: FINALIZAR OS TESTES DESSA VIEW
        if user_is_aluno(request.user):
            aluno = Aluno.objects.get(usuario=request.user)
            if aluno.reservas < MAX_RESERVAS_POR_USUARIO[0][1]:
                livro = Livro.objects.get(id=id_livro) # type: ignore
                Reserva.objects.create(
                    usuario=request.user,
                    livro=livro,
                    data_reserva=date.today(), 
                    ativo=True
                )
                return HttpResponse("Reserva Realizada com Sucesso.")
            else:
                return HttpResponse("Nao eh possivel fazer mais reservas. Usuário já atingiu o numero máximo de reservas.")

        elif user_is_professor(request.user):
            professor = Professor.objects.get(usuario=request.user)
            if professor.reservas < MAX_RESERVAS_POR_USUARIO[1][1]:
                livro = Livro.objects.get(id=id_livro) # type: ignore
                Reserva.objects.create(
                    usuario=request.user,
                    livro=livro,
                    data_reserva=date.today(), 
                    ativo=True
                )
                return HttpResponse("Reserva Realizada com Sucesso.")
            else:
                return HttpResponse("Nao eh possivel fazer mais reservas. Usuário já atingiu o numero máximo de reservas.")
        
        elif user_is_funcionario(request.user):
            funcionario = Funcionario.objects.get(usuario=request.user)
            if funcionario.reservas < MAX_RESERVAS_POR_USUARIO[2][1]:
                livro = Livro.objects.get(id=id_livro) # type: ignore
                Reserva.objects.create(
                    usuario=request.user,
                    livro=livro,
                    data_reserva=date.today(), 
                    ativo=True
                )
                return HttpResponse("Reserva Realizada com Sucesso.")
            else:
                return HttpResponse("Nao eh possivel fazer mais reservas. Usuário já atingiu o numero máximo de reservas.")
    else:
        # Retorna mensagem de erro
        return HttpResponse("Erro! Usuário não autenticado.")

def listar_reservas(request:HttpRequest):
    reservas = Reserva.objects.filter(usuario=request.user).exists()
    if reservas:
        reservas = Reserva.objects.filter(usuario=request.user)
        template_name = "livro/listar_reservas.html"
        return render(request, template_name=template_name, context={'reservas':reservas})
    else:
        return HttpResponse('O Usuário ainda não fez nenhuma reserva.')

def ler_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    return HttpResponse('View de ler reserva')

def atualizar_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    return HttpResponse('View de atualizar reserva')

def deletar_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    return HttpResponse('View de deletar reserva')

# Views de Emprestimo

def criar_emprestimo(request: HttpRequest) -> HttpResponse:
    return HttpResponse('View de criar emprestimo.')

def listar_emprestimos(request: HttpRequest) -> HttpResponse:
    return HttpResponse("View de listar emprestimos")

def ler_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('Views de ler emprestimo')

def atualizar_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('View de atualizar emprestimo')

def deletar_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('View de deletar emprestimo')