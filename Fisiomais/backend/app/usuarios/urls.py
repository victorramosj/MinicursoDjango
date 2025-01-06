from django.urls import path
from .views import custom_login, cadastrar_cliente, cadastrar_colaborador, escolher_tipo_usuario
from django.contrib.auth.views import LogoutView  # Importe a view padrão de logout

urlpatterns = [
    path('login/', custom_login, name='login'),  # URL de login
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('cadastro/cliente/', cadastrar_cliente, name='cadastrar_cliente'),
    path('cadastro/colaborador/', cadastrar_colaborador, name='cadastrar_colaborador'),
    path('escolher_tipo/', escolher_tipo_usuario, name='escolher_tipo_usuario'),
]
