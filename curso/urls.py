from django.urls import path
from curso import views

app_name = 'curso'
urlpatterns = [
    path('cursos/', views.index, name='index'),
    path('criar-curso/', views.criar_curso, name='criar-curso'),
    path('ler-curso/<int:cid>/', views.ler_curso, name='ler-curso'),
    path('atualizar-curso/<int:cid>/', views.atualizar_curso, name='atualizar-curso'),
    path('deletar-curso/<int:cid>/', views.deletar_curso, name='deletar-curso'),
]