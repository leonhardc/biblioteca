from django.urls import path
from administrador import views

app_name = 'administrador'
urlpatterns = [
    # Páginas de administrador
    path('', views.dashboard_admin, name='dashboard-admin'),
    path('usuarios/', views.dashboard_admin_usuarios, name='dashboard-admin-usuarios'),
    # Urls para alunos
    path('criar-aluno/', views.criar_aluno, name='criar_aluno'),
    path('informacoes-aluno/<int:uid>/', views.informacoes_aluno, name='informacoes_aluno'),
    path('atualizar-aluno/<int:uid>/', views.atualizar_infomacoes_aluno, name='atualizar_aluno'),
    path('deletar-aluno/<int:uid>/', views.deletar_aluno, name='deletar_aluno'),
    # Urls de professor
    path('criar-professor/', views.criar_professor, name='criar_professor'),
    path('informacoes-professor/<int:uid>/', views.informacoes_professor, name='informacoes_professor'),
    path('atualizar-professor/<int:uid>/', views.atualizar_informacoes_professor, name='atualizar_professor'),
    path('deletar-professor/<int:uid>/', views.deletar_professor, name='deletar_professor'),
    # Urls de funcionario
    path('criar-funcionario/', views.criar_funcionario, name='criar_funcionario'),
    path('informacoes-funcionario/<int:uid>/', views.informacoes_funcionario, name='informacoes_funcionario'),
    path('atualizar-funcionario/<int:uid>/', views.atualizar_informacoes_funcionario, name='atualizar_funcionario'),
    path('deletar-funcionario/<int:uid>/', views.deletar_funcionario, name='deletar_funcionario'),
    # Urls de livros
    path('livros/', views.dashboard_admin_livros, name='dashboard-admin-livros'),
    path('criar-livro/', views.criar_livro, name='criar_livro'),
    path('informacoes-livro/<int:lid>/', views.informacoes_livro, name='informacoes_livro'),
    path('atualizar-livro/<int:lid>/', views.atualizar_informacoes_livro, name='atualizar_livro'),
    path('deletar-livro/<int:lid>/', views.deletar_livro, name='deletar_livro'),
    ## Urls Autor
    path('criar-autor/', views.criar_autor, name='criar_autor'),
    path('informacoes-autor/<int:aid>/', views.informacoes_autor, name='informacoes_autor'),
    path('atualizar-autor/<int:aid>/', views.atualizar_informacoes_autor, name='atualizar_autor'),
    path('deletar-autor/<int:aid>/', views.deletar_autor, name='deletar_autor'),
    ## Urls Categoria
    path('criar-categoria/', views.criar_categoria, name='criar_categoria'),
    path('informacoes-categoria/<int:cid>/', views.informacoes_categoria, name='informacoes_categoria'),
    path('atualizar-categoria/<int:cid>/', views.atualizar_informacoes_categoria, name='atualizar_categoria'),
    path('deletar-categoria/<int:cid>/', views.deletar_categoria, name='deletar_categoria'),
    ## Urls de Reserva
    path('criar-reserva/', views.criar_reserva, name='criar_reserva'),
    path('informacoes-reserva/<int:cid>/', views.informacoes_reserva, name='informacoes_reserva'),
    path('atualizar-reserva/<int:cid>/', views.atualizar_informacoes_reserva, name='atualizar_reserva'),
    path('deletar-reserva/<int:cid>/', views.deletar_reserva, name='deletar_reserva'),
    ## Urls de Emprestimo
    path('criar-emprestimo/', views.criar_emprestimo, name='criar_emprestimo'),
    path('informacoes-emprestimo/<int:eid>/', views.informacoes_emprestimo, name='informacoes_emprestimo'),
    path('atualizar-emprestimo/<int:eid>/', views.atualizar_informacoes_emprestimo, name='atualizar_emprestimo'),
    path('deletar-emprestimo/<int:eid>/', views.deletar_emprestimo, name='deletar_emprestimo'),
    # Urls de Curso
    path('cursos/', views.dashboard_admin_cursos, name='dashboard-admin-cursos'),
    path('criar_curso', views.criar_curso, name='criar_curso'),
    path('informacoes_curso/<int:cid>/', views.informacoes_curso, name='informacoes_curso'),
    path('atualizar-curso/<int:cid>/', views.atualizar_informacoes_curso, name='atualizar_curso'),
    path('deletar-curso/<int:cid>/', views.deletar_curso, name='deletar_curso'),
]
