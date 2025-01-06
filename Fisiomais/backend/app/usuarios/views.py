from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib import messages



def custom_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Autentica o usuário
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                # Verifica o tipo de usuário (role) e redireciona
                if hasattr(user, 'colaborador'):  # Verifica se o usuário tem um colaborador associado
                    if user.colaborador.is_admin:
                        return redirect('/admin')  # Redireciona para a área de administração
                    else:
                        return redirect('home')  # Redireciona para a página inicial (colaborador)
                elif hasattr(user, 'cliente'):  # Verifica se o usuário tem um cliente associado
                    return redirect('home')  # Redireciona para a página inicial (cliente)
                else:
                    return redirect('home')  # Caso genérico
            else:
                # Erro de autenticação
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    # Passando o tipo de usuário (role) para o template
    return render(request, 'usuarios/login.html', {'form': form, 'role': None if not request.user.is_authenticated else ('cliente' if hasattr(request.user, 'cliente') else 'admin')})

def custom_logout(request):
    logout(request)  # Realiza o logout do usuário
    return redirect('/')  # Redireciona para a página inicial após logout


from .forms import ClienteForm, ColaboradorForm  # Supondo que criemos formulários para ambos


def escolher_tipo_usuario(request):
    """
    Exibe a página para o usuário escolher entre Cliente ou Colaborador.
    """
    if request.method == "POST":
        tipo = request.POST.get("tipo_usuario")
        if tipo == "cliente":
            return redirect('cadastrar_cliente')
        elif tipo == "colaborador":
            return redirect('cadastrar_colaborador')
        else:
            messages.error(request, "Escolha inválida. Por favor, selecione Cliente ou Colaborador.")
    return render(request, 'usuarios/escolher_tipo.html')



# Cadastro de Cliente
def cadastrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            cliente = form.save(commit=False)
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            cliente.user = user
            cliente.save()
            login(request, user)  # Faz o login automático após o cadastro
            messages.success(request, "Cliente cadastrado com sucesso!")

            # Passando o tipo de usuário (role) para o template de login
            role = 'cliente' if hasattr(request.user, 'cliente') else 'admin' if request.user.is_staff else None
            return render(request, 'usuarios/login.html', {'role': role})

        else:
            messages.error(request, "Erro ao cadastrar cliente. Verifique os dados fornecidos.")
    else:
        form = ClienteForm()
    return render(request, "usuarios/cadastrar_cliente.html", {"form": form})

# Cadastro de Colaborador
def cadastrar_colaborador(request):
    if request.method == "POST":
        form = ColaboradorForm(request.POST, request.FILES)
        if form.is_valid():
            colaborador = form.save(commit=False)
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            colaborador.user = user
            colaborador.save()
            login(request, user)  # Faz o login automático após o cadastro
            messages.success(request, "Colaborador cadastrado com sucesso!")

            # Passando o tipo de usuário (role) para o template de login
            role = 'colaborador' if hasattr(request.user, 'colaborador') else 'admin' if request.user.is_staff else None
            return render(request, 'usuarios/login.html', {'role': role})

        else:
            messages.error(request, "Erro ao cadastrar colaborador. Verifique os dados fornecidos.")
    else:
        form = ColaboradorForm()
    return render(request, "usuarios/cadastrar_colaborador.html", {"form": form})





