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
        paginator = Paginator(pesquisa, itens_por_pagina)
        page_number = request.GET.get("page")
        livros = paginator.get_page(page_number)
        return render(request, template_name=template_name, context={"livros": livros, 'termo_busca': termo_pesquisa})
    else:
        livros = Livro.objects.all()
        paginator = Paginator(livros, itens_por_pagina)
        page_number = request.GET.get("page")
        livros = paginator.get_page(page_number)
        return render(request, template_name=template_name, context={"livros": livros})

def listar_autores(resquest):
    pass

def listar_categorias(request):
    pass

# Implementação do CRUD para livro
def criar_livro(request):
    pass

def detalhar_livro(request, id_livro):
    pass

def atualizar_livro(request, id_livro):
    pass

def deletar_livro(request, id_livro):
    pass

# Implementação de Emprestimo e Reserva de Livros
def reservar_livro(request, id_livro, usuario):
    pass

def emprestar_livro(request, id_livro, usuario):
    pass

# CRUD para Autor
def criar_autor(request):
    pass 

def detalhar_autor(request, id_autor):
    pass 

def atualizar_autor(request, id_autor):
    pass

def deletar_autor(request, id_autor):
    pass

# CRUD para Categoria
def criar_categoria(request):
    pass

def detalhar_categoria(request, id_categoria):
    pass

def atualizar_categoria(request, id_categoria):
    pass

def deletar_categoria(request, id_categoria):
    pass