from django.urls import path
from .views import custom_login, logout  # Ajuste: usaremos custom_login

urlpatterns = [
    path('login/', custom_login, name='login'),  # A URL de login
    path('logout/', logout, name='logout'),  # A URL de logout
]
