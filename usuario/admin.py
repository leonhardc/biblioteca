from django.contrib import admin
from django.contrib.auth.models import User
from usuario.models import Aluno, Professor, Funcionario, ProfessorCurso

class AlunoAdmin(admin.ModelAdmin):
    list_display = [
        'matricula',
        'usuario',
        'nome',
        'cpf',
        'curso',
        'endereco',
        'ingresso',
        'conclusao_prevista',
    ]
    search_fields = ['matricula', 'curso']
    list_display_links = ['matricula', 'usuario']
    
    def nome(self, obj):
        return obj.usuario.first_name +' '+obj.usuario.last_name

    def email(self, obj):
        usuario = User.objects.get(id=obj.usuario_id)
        return str(usuario.email)


class ProfessorAdmin(admin.ModelAdmin):
    list_display = [
        'matricula',
        'usuario',
        'nome',
        'email',
        'regime',
        'contratacao',
        'curso',
    ]
    search_fields = [
        'matricula', 
        'curso'
        ]    
    list_display_links = [
        'matricula', 
        'usuario'
        ]

    def nome(self, obj):
        return obj.usuario.first_name +' '+ obj.usuario.last_name

    def email(self, obj):
        usuario = User.objects.get(id=obj.usuario_id)
        return str(usuario.email)


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = [
        'matricula',
        'usuario',
        'nome',
        'email',
    ]
    search_fields = [
        'matricula'
        ]
    list_display_links = [
        'matricula', 
        'usuario'
        ]

    def nome(self, obj):
        return obj.usuario.first_name +' '+ obj.usuario.last_name
    
    def email(self, obj):
        usuario = User.objects.get(id=obj.usuario_id)
        return str(usuario.email)

class ProfessorCursoAdmin(admin.ModelAdmin):
    list_display = [
        'matricula_professor',
        'professor',
        'curso_matricula',
        'curso',
        'data_matricula',
    ]
    list_display_links = [
        'professor',
    ]

    def curso_matricula(self, obj):
        return obj.curso.cod_curso

    def matricula_professor(self, obj):
        return obj.professor.matricula


admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(ProfessorCurso, ProfessorCursoAdmin)


