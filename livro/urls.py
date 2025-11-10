from django.urls import path
from livro.views import *

app_name = "livro"

urlpatterns = [ # type: ignore
    # Livros
    path("listar-livros/",view=listar_livros, name="listar_livros"),
    path("criar-livro/",view=criar_livro, name="criar_livro"),
    path("detalhar-livro/<int:id_livro>/",view=detalhar_livro, name="detalhar_livro"),
    path("atualizar-livro/<int:id_livro>/",view=atualizar_livro, name="atualizar_livro"),
    path("deletar-livro/<int:id_livro>/",view=deletar_livro, name="deletar_livro"),
    path("reservar-livro/<int:id_livro>/",view=reservar_livro, name="reservar_livro"),
    path("emprestar-livro/<int:id_livro>/",view=emprestar_livro, name="emprestar_livro"),
    # Autores
    path("listar-autores/",view=listar_autores, name="listar_autores"),
    path("criar-autor/",view=criar_autor, name="criar_autor"),
    path("detalhar-autor/<int:id_autor>/",view=detalhar_autor, name="detalhar_autor"),
    path("atualizar-autor/<int:id_autor>/",view=atualizar_autor, name="atualizar_autor"),
    path("deletar-autor/<int:id_autor>/",view=deletar_autor, name="deletar_autor"),
    # Categorias
    path("listar-categorias/",view=listar_categorias, name="listar_categorias"),
    path("criar-categoria/",view=criar_categoria, name="criar_categoria"),
    path("detalhar-categoria/<int:id_categoria>/",view=detalhar_categoria, name="detalhar_categoria"),
    path("atualizar-categoria/<int:id_categoria>/",view=atualizar_categoria, name="atualizar_categoria"),
    path("deletar-categoria/<int:id_categoria>/",view=deletar_categoria, name="deletar_categoria"),
    # Reservas
    path("criar-reserva/<int:id_livro>/", view=criar_reserva, name="criar_reserva"), # type: ignore
    path("listar-reservas/", view=listar_reservas, name="listar_reservas"),
    path("ler-reserva/<int:id_reserva>/", view=ler_reserva, name="ler_reserva"),
    path("atualizar-reserva/<int:id_reserva>/", view=atualizar_reserva, name="atualizar_reserva"),
    path("deletar-reserva/<int:id_reserva>/", view=deletar_reserva, name="deletar_reserva"),
    # Emprestimos
    path('criar-emprestimo/<int:id_livro>/<int:id_usuario>/', view=criar_emprestimo, name="criar_emprestimo"), # type: ignore
    path('novo-emprestimo/', view=criar_emprestimo_formulario, name="novo_emprestimo"), # type: ignore
    path('listar-emprestimos/', view=listar_emprestimos, name="listar_emprestimos"),
    path('ler-emprestimo/<int:id_emprestimo>/', view=ler_emprestimo, name="ler_emprestimo"),
    path('atualizar-emprestimo/<int:id_emprestimo>/', view=atualizar_emprestimo, name="atualizar_emprestimo"),
    path('deletar-emprestimo/<int:id_emprestimo>/', view=deletar_emprestimo, name="deletar_emprestimo"),
]