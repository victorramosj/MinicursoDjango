from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'colaborador'):
                if user.colaborador.is_admin:
                    return redirect('admin_dashboard')  # Dashboard de administrador
                return redirect('colaborador_dashboard')  # Dashboard de colaborador
            elif hasattr(user, 'cliente'):
                return redirect('cliente_dashboard')  # Dashboard de cliente
            else:
                messages.error(request, "Usuário não possui permissões atribuídas.")
        else:
            messages.error(request, "Credenciais inválidas.")
    return render(request, 'login.html')


def custom_logout(request):
    logout(request)  # Realiza o logout do usuário
    return redirect('login')  # Redireciona para a página de login



