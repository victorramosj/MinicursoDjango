from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView  # Importe a view padrão de logout


urlpatterns = [
    path('login/', custom_login, name='login'),  # URL de login
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('cadastro/cliente/', cadastrar_cliente, name='cadastrar_cliente'),
    path('cadastro/colaborador/', cadastrar_colaborador, name='cadastrar_colaborador'),
    path('escolher_tipo/', escolher_tipo_usuario, name='escolher_tipo_usuario'),
    path('estados/', estados_view, name='estados'),
    path('cidades/<str:estado>/', cidades, name='cidades'),
    path('colaboradores/', get_colaboradores, name='get_colaboradores'),  # API para buscar colaboradores
    path('clinicas/', fetch_clinicas, name='fetch_clinicas'),
    path('clientes/', get_clientes, name='get_clientes'), 
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    
]
