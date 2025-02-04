from django.contrib import admin
from .models import Autor, Categoria, Livro, Reserva, Emprestimo

class AutorAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'cpf',
        'nacionalidade',
    ]
    search_fields = [
        'nome',
        'nacionalidade',
    ]

class CategoriaAdmin(admin.ModelAdmin):
    list_display = [
        'categoria',
        'descricao',
    ]
    search_fields = [
        'categoria',
        'descricao',
    ]

class LivroAdmin(admin.ModelAdmin):
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

    # Mudar o label do campo de 'get_autores' para 'autores'
    @admin.display(description='autores')
    def _autores(self, obj):
        return obj.get_autores()
    
    def categoria(self, obj):
        obj.categoria.categoria

class ReservaAdmin(admin.ModelAdmin):
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

class EmprestimoAdmin(admin.ModelAdmin):
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

admin.site.register(Autor, AutorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Livro, LivroAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Emprestimo, EmprestimoAdmin)