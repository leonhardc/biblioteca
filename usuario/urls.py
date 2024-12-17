from django.urls import path
from usuario import views

app_name = 'usuario'
urlpatterns = [
    path('', views.index, name='index'),
    path('entrar/', views.entrar, name='entrar'),
    path('autenticar/', views.autenticar, name='autenticar'),
    path('logout/', views.sair, name='sair'),
]