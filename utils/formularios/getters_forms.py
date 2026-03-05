# De livro.forms
from livro.models import Livro, Autor, Categoria
from django.contrib.auth.models import User

def get_categorias() -> tuple[tuple[int, str]]:
    try:
        return tuple([(categoria.id, categoria.categoria) for categoria in Categoria.objects.all()])                    # type: ignore
    except: 
        return ()                                                                                                       # type: ignore

def get_autores() -> tuple[tuple[int, str]]:
    try:
        return tuple([(autor.id, autor.nome) for autor in Autor.objects.all()])                                         # type: ignore
    except:
        return ()                                                                                                       # type: ignore

def get_livros() -> tuple[tuple[int, str]]:
    try:
        return tuple([(livro.id, livro.titulo) for livro in Livro.objects.all()])                                       # type: ignore
    except:
        return ()                                                                                                       # type: ignore

def get_usuarios() -> tuple[tuple[int, str]]:
    try:
        return tuple([(usuario.id, usuario.username) for usuario in User.objects.all()])                                # type: ignore
    except:
        return ()                                                                                                       # type: ignore