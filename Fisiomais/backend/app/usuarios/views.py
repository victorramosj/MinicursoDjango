from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from usuarios.models import Colaborador, Cliente
from .forms import LoginForm

def custom_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                
                # Define o papel do usuário (role)
                if hasattr(user, 'colaborador'):
                    if user.colaborador.is_admin:
                        role = "admin"
                    else:
                        role = "colaborador"
                elif hasattr(user, 'cliente'):
                    role = "cliente"
                else:
                    role = "desconhecido"

                # Adiciona role no objeto user
                user.role = role
                request.session['role'] = role  # Armazena na sessão caso necessário

                return redirect('/')  # Redireciona para a página inicial
            else:
                form.add_error(None, 'Usuário ou senha incorretos')
        else:
            form.add_error(None, 'Erro no formulário.')
    else:
        form = LoginForm()

    return render(request, 'home.html', {'form': form})






def custom_logout(request):
    logout(request)  # Realiza o logout do usuário
    return redirect('/')  # Redireciona para a página inicial após logout


from .forms import ClienteForm, ColaboradorForm  


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



import logging
# Configuração do logger
logger = logging.getLogger(__name__)

def cadastrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Cria o cliente e associa o usuário (feito no save do formulário)
                cliente = form.save(commit=False)
                
                # Realiza o login automático após salvar o cliente
                login(request, cliente.user)
                
                messages.success(request, "Cliente cadastrado com sucesso!")
                
                # Passando o tipo de usuário (role) para o template de login
                role = 'cliente' if hasattr(request.user, 'cliente') else 'admin' if request.user.is_staff else None
                return render(request, 'home.html', {'role': role})
            except Exception as e:
                # Log detalhado do erro
                logger.error(f"Erro ao cadastrar cliente: {str(e)}", exc_info=True)
                messages.error(request, f"Erro ao cadastrar cliente: {str(e)}")
        else:
            # Exibe os erros detalhados de validação do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    else:
        form = ClienteForm()

    return render(request, "usuarios/cadastrar_cliente.html", {"form": form})


def cadastrar_colaborador(request):
    if request.method == "POST":
        form = ColaboradorForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Cria o colaborador e associa o usuário (feito no save do formulário)
                colaborador = form.save(commit=False)
                
                # Faz login automático do colaborador após salvar
                login(request, colaborador.user)
                
                messages.success(request, "Colaborador cadastrado com sucesso!")
                return redirect("home")  # Substitua "home" pela URL de destino desejada
            except Exception as e:
                # Log detalhado do erro
                logger.error(f"Erro ao cadastrar colaborador: {str(e)}", exc_info=True)
                messages.error(request, f"Erro ao cadastrar colaborador: {str(e)}")
        else:
            # Exibe os erros detalhados de validação do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    else:
        form = ColaboradorForm()

    return render(request, "usuarios/cadastrar_colaborador.html", {"form": form})







from django.http import JsonResponse


def estados_view(request):
    try:
        # Faz a requisição para obter a lista de estados
        response = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
        response.raise_for_status()  # Verifica se a resposta foi bem-sucedida
        
        # Ordena os estados pelo nome
        estados = response.json()
        estados_ordenados = sorted(estados, key=lambda x: x['nome'])

        # Retorna a lista de estados em formato JSON
        return JsonResponse(estados_ordenados, safe=False)
    
    except requests.exceptions.RequestException as e:
        # Retorna um erro em caso de falha na requisição
        return JsonResponse({"error": str(e)}, status=500)

# Função para obter cidades de um estado específico
def cidades(request, estado):
    try:
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado}/municipios"
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a resposta foi bem-sucedida
        cidades = response.json()
        cidades_ordenadas = sorted(cidades, key=lambda x: x['nome'])
        return JsonResponse(cidades_ordenadas, safe=False)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse

def get_colaboradores(request):
    clinica_id = request.GET.get('clinica_id')
    servico_id = request.GET.get('servico_id')
    
    if clinica_id and servico_id:
        colaboradores = Colaborador.objects.filter(
            clinica_id=clinica_id,
            servicos_relacionados__servico_id=servico_id
        ).distinct()
        colaboradores_data = [
            {'id': c.id, 'nome': c.nome} for c in colaboradores
        ]
        return JsonResponse({'colaboradores': colaboradores_data})
    
    return JsonResponse({'colaboradores': []})


from django.http import JsonResponse
from .models import Clinica

def fetch_clinicas(request):
    clinicas = Clinica.objects.all()
    clinicas_data = [{'id': clinica.id, 'nome': clinica.nome} for clinica in clinicas]
    return JsonResponse({'clinicas': clinicas_data})

def get_clientes(request):
    clientes = Cliente.objects.all()
    clientes_data = [
        {
            'id': cliente.id,
            'nome': cliente.nome
        }
        for cliente in clientes
    ]
    return JsonResponse({'clientes': clientes_data})