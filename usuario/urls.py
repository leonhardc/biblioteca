from django.urls import path
from usuario import views

app_name = 'usuario'
urlpatterns = [
    path('', views.index, name='index'),
    path('entrar/', views.entrar, name='entrar'),
    path('autenticar/', views.autenticar, name='autenticar'),
    path('sair/', views.sair, name='sair'),
    # Páginas de administrador
    # path('admin-page/', views.admin_page, name='admin-page'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard-admin/<str:model_type>/', views.admin_page, name='admin-page'),
    # CRUD de alunos
    path('listar-alunos/', views.listar_alunos, name='listar_alunos'),
    path('criar-aluno/', views.criar_aluno, name='criar-aluno'),
    path('ler-aluno/<int:uid>/', views.ler_aluno, name='ler-aluno'),
    path('atualizar-aluno/<int:uid>/', views.atualizar_aluno, name='atualizar-aluno'),
    path('deletar-aluno/<int:uid>/', views.deletar_aluno, name='deletar-aluno'),
    # CRUD de professor
    path('criar-professor/', views.criar_professor, name='criar-professor'),
    path('ler-professor/<int:uid>/', views.ler_professor, name='ler-professor'),
    path('atualizar-professor/<int:uid>/', views.atualizar_professor, name='atualizar-professor'),
    path('deletar-professor/<int:uid>/', views.deletar_professor, name='deletar-professor'),
    # CRUD de funcionario
    path('criar-funcionario/', views.criar_funcionario, name='criar-funcionario'),
    path('ler-funcionario/<int:uid>/', views.ler_funcionario, name='ler-funcionario'),
    path('atualizar-funcionario/<int:uid>/', views.atualizar_funcionario, name='atualizar-funcionario'),
    path('deletar-funcionario/<int:uid>/', views.deletar_funcionario, name='deletar-funcionario'),
]