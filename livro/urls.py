from django.urls import path
from livro.views import *

app_name = "livro"

urlpatterns = [
    # Livros
    path("listar-livros/",view=listar_livros, name="listar-livros"),
    path("criar-livro/",view=criar_livro, name="criar-livro"),
    path("detalhar-livro/<int:id_livro>/",view=detalhar_livro, name="detalhar-livro"),
    path("atualizar-livro/<int:id_livro>/",view=atualizar_livro, name="atualizar-livro"),
    path("deletar-livro/<int:id_livro>/",view=deletar_livro, name="deletar-livro"),
    path("reservar-livro/<int:id_livro>/",view=reservar_livro, name="reservar-livro"),
    path("emprestar-livro/<int:id_livro>/",view=emprestar_livro, name="emprestar-livro"),
    # Autores
    path("listar-autores/",view=listar_autores, name="listar-autores"),
    path("criar-autor/",view=criar_autor, name="criar-autor"),
    path("detalhar-autor/<int:id_autor>/",view=detalhar_autor, name="detalhar-autor"),
    path("atualizar-autor/<int:id_autor>/",view=atualizar_autor, name="atualizar-autor"),
    path("deletar-autor/<int:id_autor>/",view=deletar_autor, name="deletar-autor"),
    # Categorias
    path("listar-categorias/",view=listar_categorias, name="listar-categorias"),
    path("criar-categoria/",view=criar_categoria, name="criar-categoria"),
    path("detalhar-categoria/<int:id_categoria>/",view=detalhar_categoria, name="detalhar-categoria"),
    path("atualizar-categoria/<int:id_categoria>/",view=atualizar_categoria, name="atualizar-categoria"),
    path("deletar-categoria/<int:id_categoria>/",view=deletar_categoria, name="deletar-categoria"),
]