from django.urls import path
from usuario import views

app_name = 'usuario'
urlpatterns = [                                                                                                         # type: ignore
    path('', views.index, name='index'),
    path('entrar/', views.entrar, name='entrar'),                                                                       # type: ignore
    path('autenticar/', views.autenticar, name='autenticar'),                                                           # type: ignore
    path('sair/', views.sair, name='sair'),

    # CRUD de alunos
    path('listar-alunos/', views.listar_alunos, name='listar-alunos'),
    path('pagina_inicial_aluno/<int:uid>/', views.pagina_inicial_aluno, name='pagina_inicial_aluno'),
    path('criar-aluno/', views.criar_aluno, name='criar-aluno'),                                                        # type: ignore
    path('ler-aluno/', views.ler_aluno, name='ler-aluno'),                                                    # type: ignore
    path('atualizar-aluno/<int:uid>/', views.atualizar_aluno, name='atualizar-aluno'),                                  # type: ignore
    path('deletar-aluno/<int:uid>/', views.deletar_aluno, name='deletar-aluno'),                                        # type: ignore
    path('detalhes-aluno/<int:uid>/', views.detalhes_aluno, name='detalhes-aluno'),                                     # type: ignore
    path('dashboard-aluno/', views.dashaboard_aluno, name='dashboard_aluno'), # type: ignore
    # CRUD de professor
    path('criar-professor/', views.criar_professor, name='criar-professor'), 
    path('pagina_inicial_professor/<int:uid>/', views.pagina_inicial_professor, name='pagina_inicial_professor'),                                           # type: ignore
    path('ler-professor/<int:uid>/', views.ler_professor, name='ler-professor'),                                        # type: ignore
    path('atualizar-professor/<int:uid>/', views.atualizar_professor, name='atualizar-professor'),                      # type: ignore
    path('deletar-professor/<int:uid>/', views.deletar_professor, name='deletar-professor'),                            # type: ignore
    path('detalhes-professor/<int:uid>/', views.detalhes_professor, name='detalhes-professor'),                         # type: ignore
    # CRUD de funcionario
    path('criar-funcionario/', views.criar_funcionario, name='criar-funcionario'),  
    path('pagina_inicial_funcionario/<int:uid>/', views.pagina_inicial_funcionario, name='pagina_inicial_funcionario'),                                    # type: ignore
    path('ler-funcionario/<int:uid>/', views.ler_funcionario, name='ler-funcionario'),                                  # type: ignore
    path('atualizar-funcionario/<int:uid>/', views.atualizar_funcionario, name='atualizar-funcionario'),                # type: ignore
    path('deletar-funcionario/<int:uid>/', views.deletar_funcionario, name='deletar-funcionario'),                      # type: ignore
    path('detalhes-funcionario/<int:uid>/', views.detalhes_funcionario, name='detalhes-funcionario'),                   # type: ignore
    path('buscar-usuario/', views.buscar_usuario, name='buscar_usuario'),                                                 # type: ignore
]