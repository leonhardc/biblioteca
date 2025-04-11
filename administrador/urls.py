from django.urls import path
from administrador import views

app_name = 'administrador'
urlpatterns = [
    # Páginas de administrador
    path('', views.dashboard_admin, name='dashboard-admin'),
    path('usuarios/', views.dashboard_admin_usuarios, name='dashboard-admin-usuarios'),
    path('atualizar-aluno/<int:uid>/', views.atualizar_infomacoes_aluno, name='atualizar_aluno'),
    path('atualizar-professor/<int:uid>/', views.atualizar_informacoes_professor, name='atualizar_professor'),
    path('deletar-aluno/<int:uid>/', views.deletar_aluno, name='deletar_aluno'),
    path('deletar-professor/<int:uid>/', views.deletar_professor, name='deletar_professor'),
    path('livros/', views.dashboard_admin_livros, name='dashboard-admin-livros'),
    path('cursos/', views.dashboard_admin_cursos, name='dashboard-admin-cursos'),
]
