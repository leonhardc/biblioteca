from django.urls import path
from administrador import views

app_name = 'administrador'
urlpatterns = [
    # Páginas de administrador
    path('', views.dashboard_admin, name='dashboard-admin'),
    path('usuarios/', views.dashboard_admin_usuarios, name='dashboard-admin-usuarios'),
    # Views para alunos
    path('criar-aluno/', views.criar_aluno, name='criar_aluno'),
    path('informacoes-aluno/<int:uid>/', views.informacoes_aluno, name='informacoes_aluno'),
    path('atualizar-aluno/<int:uid>/', views.atualizar_infomacoes_aluno, name='atualizar_aluno'),
    path('deletar-aluno/<int:uid>/', views.deletar_aluno, name='deletar_aluno'),
    # Views de professor
    path('criar-professor/', views.criar_professor, name='criar_professor'),
    path('informacoes-professor/<int:uid>/', views.informacoes_professor, name='informacoes_professor'),
    path('atualizar-professor/<int:uid>/', views.atualizar_informacoes_professor, name='atualizar_professor'),
    path('deletar-professor/<int:uid>/', views.deletar_professor, name='deletar_professor'),
    # Views de funcionario
    path('criar-funcionario/', views.criar_funcionario, name='criar_funcionario'),
    path('informacoes-funcionario/<int:uid>/', views.informacoes_funcionario, name='informacoes_funcionario'),
    path('atualizar-funcionario/<int:uid>/', views.atualizar_informacoes_funcionario, name='atualizar_funcionario'),
    path('deletar-funcionario/<int:uid>/', views.deletar_funcionario, name='deletar_funcionario'),
    path('livros/', views.dashboard_admin_livros, name='dashboard-admin-livros'),
    path('cursos/', views.dashboard_admin_cursos, name='dashboard-admin-cursos'),
]
