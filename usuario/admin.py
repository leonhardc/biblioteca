from django.contrib import admin
from django.contrib.auth.models import User
from usuario.models import Aluno, Professor, Funcionario

class AlunoAdmin(admin.ModelAdmin):
    list_display = [
        'matricula', 
        'usuario', 
        'usuario_email',
        'curso', 
        'cpf', 
        'ingresso', 
        'conclusao_prevista'
        ]
    search_fields = ['matricula', 'curso']
    list_display_links = ['matricula', 'usuario']
    def usuario_email(self, obj):
        usuario = User.objects.get(id=obj.usuario_id)
        return str(usuario.email)


class ProfessorAdmin(admin.ModelAdmin):
    list_display = [
        'matricula', 
        'usuario',
        'usuario_email', 
        'curso', 
        'cpf', 
        'contratacao', 
        'regime'
        ]
    search_fields = [
        'matricula', 
        'curso'
        ]    
    list_display_links = [
        'matricula', 
        'usuario'
        ]

    def usuario_email(self, obj):
        usuario = User.objects.get(id=obj.usuario_id)
        return str(usuario.email)


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = [
        'matricula',
        'usuario',
        'usuario_email',
    ]
    search_fields = [
        'matricula'
        ]
    list_display_links = [
        'matricula', 
        'usuario'
        ]

    def usuario_email(self, obj):
        usuario = User.objects.get(id=obj.usuario_id)
        return str(usuario.email)


admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)

