from django.urls import path
from administrador import views

app_name = 'administrador'
urlpatterns = [
    # Páginas de administrador
    path('', views.dashboard_admin, name='dashboard-admin'),
    path('usuarios/', views.dashboard_admin_usuarios, name='dashboard-admin-usuarios'),
    path('livros/', views.dashboard_admin_livros, name='dashboard-admin-livros'),
    path('cursos/', views.dashboard_admin_cursos, name='dashboard-admin-cursos'),
]
