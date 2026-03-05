from django.contrib import admin
from .models import Autor, Categoria, Livro, Reserva, Emprestimo


class AutorAdmin(admin.ModelAdmin): # type: ignore
    list_display = [
        'nome',
        'sobrenome',
        'nascimento',
        'email_de_contato',
        'nacionalidade',
        'sexo',
    ]
    search_fields = [
        'nome',
        'nascimento',
        'email_de_contato',
        'nacionalidade',
    ]
    list_per_page = 20


class CategoriaAdmin(admin.ModelAdmin): # type: ignore
    list_display = [
        'categoria',
        'descricao',
    ]
    search_fields = [
        'categoria',
        'descricao',
    ]
    list_per_page = 20


class LivroAdmin(admin.ModelAdmin): # type: ignore
    list_display = [
        'isbn',
        'titulo',
        'lancamento',
        'editora',        
        'copias',        
        'categoria',        
        '_autores',        
    ]
    search_fields = [
        'isbn',
        'titulo',
        'categoria',
    ]
    list_per_page = 20

    # Mudar o label do campo de 'get_autores' para 'autores'
    @admin.display(description='autores')
    def _autores(self, obj): # type: ignore
        return obj.get_autores() # type: ignore
    
    def categoria(self, obj): # type: ignore
        obj.categoria.categoria # type: ignore

class ReservaAdmin(admin.ModelAdmin): # type: ignore
    list_display = [
        'usuario',
        'livro',
        'data_reserva',
    ]
    search_fields = [
        'usuario',
        'livro',
        'data_reserva',
    ]
    list_per_page = 20

class EmprestimoAdmin(admin.ModelAdmin): # type: ignore
    list_display = [
        'usuario',
        'livro',
        'data_emprestimo',
        'data_devolucao',
    ]
    search_fields = [
        'usuario',
        'livro',
        'data_emprestimo',
    ]
    list_per_page = 20

# admin.site.register(Autor, AutorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Livro, LivroAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Emprestimo, EmprestimoAdmin)