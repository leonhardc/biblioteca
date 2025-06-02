from django.urls import path
from administrador import views

app_name = 'administrador'
urlpatterns = [                                                                                                         # type: ignore
    # Páginas de administrador
    path('', views.dashboard_admin, name='dashboard-admin'),                                                            # type: ignore
    path('usuarios/', views.dashboard_admin_usuarios, name='dashboard-admin-usuarios'),                                 # type: ignore
    # Urls para alunos
    path('criar-aluno/', views.criar_aluno, name='criar_aluno'),                                                        # type: ignore
    path('informacoes-aluno/<int:uid>/', views.informacoes_aluno, name='informacoes_aluno'),                            # type: ignore
    path('atualizar-aluno/<int:uid>/', views.atualizar_infomacoes_aluno, name='atualizar_aluno'),                       # type: ignore
    path('deletar-aluno/<int:uid>/', views.deletar_aluno, name='deletar_aluno'),
    # Urls de professor
    path('criar-professor/', views.criar_professor, name='criar_professor'),                                            # type: ignore
    path('informacoes-professor/<int:uid>/', views.informacoes_professor, name='informacoes_professor'),                # type: ignore
    path('atualizar-professor/<int:uid>/', views.atualizar_informacoes_professor, name='atualizar_professor'),          # type: ignore
    path('deletar-professor/<int:uid>/', views.deletar_professor, name='deletar_professor'),
    # Urls de funcionario
    path('criar-funcionario/', views.criar_funcionario, name='criar_funcionario'),                                      # type: ignore
    path('informacoes-funcionario/<int:uid>/', views.informacoes_funcionario, name='informacoes_funcionario'),          # type: ignore
    path('atualizar-funcionario/<int:uid>/', views.atualizar_informacoes_funcionario, name='atualizar_funcionario'),    # type: ignore
    path('deletar-funcionario/<int:uid>/', views.deletar_funcionario, name='deletar_funcionario'),
    # Urls de livros
    path('livros/', views.dashboard_admin_livros, name='dashboard-admin-livros'),                                       # type: ignore
    path('criar-livro/', views.criar_livro, name='criar_livro'),                                                        # type: ignore
    path('informacoes-livro/<int:lid>/', views.informacoes_livro, name='informacoes_livro'),                            # type: ignore
    path('atualizar-livro/<int:lid>/', views.atualizar_informacoes_livro, name='atualizar_livro'),                      # type: ignore
    path('deletar-livro/<int:lid>/', views.deletar_livro, name='deletar_livro'),                                        # type: ignore
    ## Urls Autor
    path('criar-autor/', views.criar_autor, name='criar_autor'),                                                        # type: ignore
    path('informacoes-autor/<int:aid>/', views.informacoes_autor, name='informacoes_autor'),                            # type: ignore
    path('atualizar-autor/<int:aid>/', views.atualizar_informacoes_autor, name='atualizar_autor'),                      # type: ignore
    path('deletar-autor/<int:aid>/', views.deletar_autor, name='deletar_autor'),                                        # type: ignore
    ## Urls Categoria
    path('criar-categoria/', views.criar_categoria, name='criar_categoria'),                                            # type: ignore
    path('informacoes-categoria/<int:cid>/', views.informacoes_categoria, name='informacoes_categoria'),                # type: ignore
    path('atualizar-categoria/<int:cid>/', views.atualizar_informacoes_categoria, name='atualizar_categoria'),          # type: ignore
    path('deletar-categoria/<int:cid>/', views.deletar_categoria, name='deletar_categoria'),                            # type: ignore
    ## Urls de Reserva
    path('criar-reserva/', views.criar_reserva, name='criar_reserva'),                                                  # type: ignore
    path('informacoes-reserva/<int:cid>/', views.informacoes_reserva, name='informacoes_reserva'),                      # type: ignore
    path('atualizar-reserva/<int:cid>/', views.atualizar_informacoes_reserva, name='atualizar_reserva'),                # type: ignore
    path('deletar-reserva/<int:cid>/', views.deletar_reserva, name='deletar_reserva'),                                  # type: ignore
    ## Urls de Emprestimo
    path('criar-emprestimo/', views.criar_emprestimo, name='criar_emprestimo'),                                         # type: ignore
    path('informacoes-emprestimo/<int:eid>/', views.informacoes_emprestimo, name='informacoes_emprestimo'),             # type: ignore
    path('atualizar-emprestimo/<int:eid>/', views.atualizar_informacoes_emprestimo, name='atualizar_emprestimo'),       # type: ignore
    path('deletar-emprestimo/<int:eid>/', views.deletar_emprestimo, name='deletar_emprestimo'),                         # type: ignore
    # Urls de Curso
    path('cursos/', views.dashboard_admin_cursos, name='dashboard-admin-cursos'),                                       # type: ignore
    path('criar_curso', views.criar_curso, name='criar_curso'),                                                         # type: ignore
    path('informacoes_curso/<int:cid>/', views.informacoes_curso, name='informacoes_curso'),                            # type: ignore
    path('atualizar-curso/<int:cid>/', views.atualizar_informacoes_curso, name='atualizar_curso'),                      # type: ignore
    path('deletar-curso/<int:cid>/', views.deletar_curso, name='deletar_curso'),                                        # type: ignore
]
