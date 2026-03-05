from django.urls import path
from notificacao import views

app_name = 'notificacao'
urlpatterns = [
    path('notificacoes/<int:id_usuario>/', views.mostrar_notificacoes, name='notificacoes'),
    path('notificacao/<int:id_notificacao>/', views.detalhe_notificacao, name='detalhe_notificacao'),
    path('deletar/<int:id_notificacao>/', views.deletar_notificacao, name='deletar_notificacao'),
]