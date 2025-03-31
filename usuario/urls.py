from django.urls import path
from usuario import views

app_name = 'usuario'
urlpatterns = [
    path('', views.index, name='index'),
    path('entrar/', views.entrar, name='entrar'),
    path('autenticar/', views.autenticar, name='autenticar'),
    path('sair/', views.sair, name='sair'),

    # CRUD de alunos
    path('listar-alunos/', views.listar_alunos, name='listar-alunos'),
    path('criar-aluno/', views.criar_aluno, name='criar-aluno'),
    path('ler-aluno/<int:uid>/', views.ler_aluno, name='ler-aluno'),
    path('atualizar-aluno/<int:uid>/', views.atualizar_aluno, name='atualizar-aluno'),
    path('deletar-aluno/<int:uid>/', views.deletar_aluno, name='deletar-aluno'),
    path('detalhes-aluno/<int:uid>/', views.detalhes_aluno, name='detalhes-aluno'),
    # CRUD de professor
    path('criar-professor/', views.criar_professor, name='criar-professor'),
    path('ler-professor/<int:uid>/', views.ler_professor, name='ler-professor'),
    path('atualizar-professor/<int:uid>/', views.atualizar_professor, name='atualizar-professor'),
    path('deletar-professor/<int:uid>/', views.deletar_professor, name='deletar-professor'),
    path('detalhes-professor/<int:uid>/', views.detalhes_professor, name='detalhes-professor'),
    # CRUD de funcionario
    path('criar-funcionario/', views.criar_funcionario, name='criar-funcionario'),
    path('ler-funcionario/<int:uid>/', views.ler_funcionario, name='ler-funcionario'),
    path('atualizar-funcionario/<int:uid>/', views.atualizar_funcionario, name='atualizar-funcionario'),
    path('deletar-funcionario/<int:uid>/', views.deletar_funcionario, name='deletar-funcionario'),
    path('detalhes-funcionario/<int:uid>/', views.detalhes_funcionario, name='detalhes-funcionario'),
]