from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from .models import Livro
from django.db.models import Q


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