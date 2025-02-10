from django.contrib import admin
from curso.models import Curso

class CursoAdmin(admin.ModelAdmin):
    list_display = [
        'cod_curso',
        'curso',
        'descricao',
        'turno',
    ]
    search_fields = [
        'cod_curso',
        'curso',
    ]
    list_display_links = [
        'cod_curso',
    ]
    list_per_page = 20

admin.site.register(Curso, CursoAdmin)