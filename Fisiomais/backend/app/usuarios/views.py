from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Colaborador, Cliente

@api_view(['POST'])
def login(request):
    email = request.data.get('email', '')
    senha = request.data.get('senha', '')

    # Autenticar o usuário utilizando o e-mail
    user = authenticate(username=email, password=senha)
    
    if user is not None:
        # Gerar o refresh token e access token
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        # Verificar se é um colaborador
        colaborador = Colaborador.objects.filter(user=user).first()
        if colaborador:
            response_data = {
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
                "userId": colaborador.id,
                "name": colaborador.user.first_name,
                "photo": colaborador.photo.url if colaborador.photo else "",
                "role": "admin" if colaborador.user.is_staff else "colaborador",
                "email_confirmado": True  # Colaboradores têm email confirmado
            }
            return Response(response_data, status=200)

        # Verificar se é um cliente
        cliente = Cliente.objects.filter(user=user).first()
        if cliente:
            email_confirmado = cliente.user.emailaddress_set.filter(verified=True).exists()
            response_data = {
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
                "userId": cliente.id,
                "name": cliente.user.first_name,
                "photo": cliente.photo.url if cliente.photo else "",
                "role": "cliente",
                "email_confirmado": email_confirmado
            }
            return Response(response_data, status=200)

    return Response({"message": "Credenciais inválidas"}, status=401)




@api_view(['POST'])
def logout(request):
    """
    Realiza o logout do usuário, invalidando a sessão.
    """
    logout(request)  # Realiza o logout do usuário
    return Response({"message": "Logout realizado com sucesso"}, status=200)
