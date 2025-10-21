from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from .models import Livro

# Método de Listar Livros, Autores e Categorias
def listar_livros(request: HttpRequest) -> HttpResponse:
    template_name = "livro/livros.html"
    livros = Livro.objects.all()
    paginator = Paginator(livros, 20)
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