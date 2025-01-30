
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import logging
from .models import Agendamento, Cliente, Colaborador, Servico, Clinica, Plano
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages  # Para exibir mensagens no redirecionamento
from .forms import AgendamentoEditForm


# Configuração do logger
logger = logging.getLogger(__name__)

@login_required
def agendar(request):
    if request.method == 'POST':
        print("Recebido POST request com dados:", request.POST)

        try:
            # Extrair os dados diretamente do request.POST            
            cliente_id = request.POST.get('cliente')
            colaborador_id = request.POST.get('colaborador')
            servico_id = request.POST.get('servico')
            plano_id = request.POST.get('plano', None)  # Plano pode ser None
            data = request.POST.get('data')
            hora = request.POST.get('hora')

            # Imprimir os dados recebidos
            print(f"cliente_id: {cliente_id}, colaborador_id: {colaborador_id}, servico_id: {servico_id}, plano_id: {plano_id}, data: {data}, hora: {hora}")
            
            plano = None if not plano_id else Plano.objects.get(id=plano_id)
            # Verificar se data ou hora são inválidas
            if not data or not hora:
                return JsonResponse({'error': 'Data ou hora não fornecida'}, status=400)

            # Combina a data e a hora recebidas
            data_e_hora_str = data + ' ' + hora
            try:
                # Converte a string para o formato datetime
                data_e_hora = datetime.strptime(data_e_hora_str, '%Y-%m-%d %H:%M')
                # Torna a data e hora timezone-aware
                data_e_hora = timezone.make_aware(data_e_hora)
            except ValueError as e:
                print("Erro ao converter data e hora:", str(e))
                return JsonResponse({'error': f'Formato de data ou hora inválido: {str(e)}'}, status=400)

            # Verificar se todos os dados obrigatórios foram preenchidos
            if not cliente_id or not colaborador_id or not servico_id or not data_e_hora:
                return JsonResponse({'error': 'Faltam dados obrigatórios.'}, status=400)

            try:
                colaborador = Colaborador.objects.get(id=colaborador_id)
            except Colaborador.DoesNotExist:
                print("Colaborador não encontrado:", colaborador_id)
                return JsonResponse({'error': 'Colaborador não encontrado'}, status=404)

            # Buscar objetos relacionados
            try:
                cliente = Cliente.objects.get(id=cliente_id)
            except Cliente.DoesNotExist:
                print("Cliente não encontrado:", cliente_id)
                return JsonResponse({'error': 'Cliente não encontrado'}, status=404)
            
              # Verificar se o cliente já tem uma clínica associada
            if cliente.clinica is None:
                # Se não tiver clínica, associar a clínica do colaborador
                cliente.clinica = colaborador.clinica
                cliente.save()  # Salvar a clínica no cliente
                print(f"Clinica {colaborador.clinica.nome} associada ao cliente {cliente.nome}")

            
            try:
                servico = Servico.objects.get(id=servico_id)
            except Servico.DoesNotExist:
                print("Serviço não encontrado:", servico_id)
                return JsonResponse({'error': 'Serviço não encontrado'}, status=404)
                               

            # Criar o agendamento
            agendamento = Agendamento.objects.create(                
                cliente=cliente,
                colaborador=colaborador,
                servico=servico,
                plano=plano,
                data_e_hora=data_e_hora
            )
            print("Agendamento criado com sucesso:", agendamento)

            # Adicionar mensagem de sucesso
            messages.success(request, 'Agendamento realizado com sucesso!')
            # Redirecionar para a página de visualizar agendamentos
            return HttpResponseRedirect(f'{reverse("visualizar_agendamentos")}?pesquisa_tipo=agendamento&pesquisa_valor={agendamento.id}')
        except Exception as e:
            print("Erro inesperado ao criar agendamento:", str(e))
            return render(request, 'agendar.html', {'error_message': 'Ocorreu um erro ao criar o agendamento. Por favor, tente novamente.'})

    return render(request, 'agendar.html')



def get_servicos(request):
    # Buscar todos os serviços cadastrados
    servicos = Servico.objects.all()
    # Criar uma lista de dicionários com os dados necessários
    servicos_data = [{'id': servico.id, 'nome_servico': servico.nome_servico, 'descricao': servico.descricao, 'valor': str(servico.valor), 'tipo_servico': servico.tipo_servico.tipo} for servico in servicos]
    
    return JsonResponse({'servicos': servicos_data})


from django.http import JsonResponse
from .models import Servico

# API para buscar planos disponíveis para um serviço específico
def get_planos(request, servico_id):
    try:
        servico = Servico.objects.get(id=servico_id)
        
        # Busca todos os planos relacionados ao serviço
        planos = servico.planos.all()
        
        # Verifica se existem planos e formata corretamente
        if planos.exists():
            planos_choices = [(str(plano.id), f"Plano {plano.id} - {plano.nome} - {plano.valor} reais") for plano in planos]
        else:
            planos_choices = []

        return JsonResponse({"planos": planos_choices})
    except Servico.DoesNotExist:
        return JsonResponse({"error": "Serviço não encontrado"}, status=400)


# API para buscar horários disponíveis para o colaborador
def get_horarios(request, colaborador_id):
    horarios = Horario.objects.filter(colaborador_id=colaborador_id)
    horarios_data = [{"id": hora.id, "hora_inicio": hora.hora_inicio, "hora_fim": hora.hora_fim} for hora in horarios]
    return JsonResponse({"horarios": horarios_data})

from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Horario, Agendamento, Colaborador

# Rota para verificar os dias permitidos para o colaborador
def dias_permitidos(request, colaborador_id):
    try:
        # Verifica se o colaborador existe
        colaborador = Colaborador.objects.get(id=colaborador_id)
        
        # Buscar todos os dias da semana em que o colaborador tem horários
        dias_disponiveis = Horario.objects.filter(colaborador_id=colaborador_id).values('dia_semana').distinct()
        if not dias_disponiveis:
            return JsonResponse({"message": "Nenhum dia disponível encontrado para o colaborador."}, status=404)

        # Mapeamento dos dias da semana
        dias_map = {
            "domingo": 0,
            "segunda-feira": 1,
            "terca-feira": 2,
            "quarta-feira": 3,
            "quinta-feira": 4,
            "sexta-feira": 5,
            "sabado": 6
        }

        # Converter os dias encontrados no banco para seus valores numéricos
        dias_convertidos = [dias_map[dia['dia_semana']] for dia in dias_disponiveis if dia['dia_semana'] in dias_map]
        
        return JsonResponse({"dias_permitidos": dias_convertidos}, status=200)
    
    except Colaborador.DoesNotExist:
        return JsonResponse({"message": "Colaborador não encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"message": f"Erro ao buscar dias permitidos: {str(e)}"}, status=500)

# Função para obter os horários disponíveis para o colaborador
from django.utils import timezone

from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils.timezone import make_aware, localtime, now
from core.models import Horario, Agendamento 

# Função para obter os horários disponíveis para o colaborador
def obter_horarios_disponiveis(colaborador_id, data_obj):
    # Garante que o objeto de data seja timezone-aware
    if data_obj.tzinfo is None:
        data_obj = make_aware(data_obj)

    # Ajuste para garantir que a data esteja no fuso horário local
    data_obj = localtime(data_obj)

    dia_semana_mapeado = {
        "Monday": "segunda-feira",
        "Tuesday": "terca-feira",
        "Wednesday": "quarta-feira",
        "Thursday": "quinta-feira",
        "Friday": "sexta-feira",
        "Saturday": "sabado",
        "Sunday": "domingo"
    }

    dia_semana = data_obj.strftime("%A")
    dia_semana_mapeado = dia_semana_mapeado[dia_semana]

    # Filtra os horários do colaborador com base no dia da semana
    horarios_colaborador = Horario.objects.filter(colaborador_id=colaborador_id, dia_semana=dia_semana_mapeado)

    # Define o intervalo de data para o dia
    data_inicio = data_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    data_fim = data_obj.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Busca os agendamentos existentes
    agendamentos = Agendamento.objects.filter(
        colaborador_id=colaborador_id,
        data_e_hora__range=[data_inicio, data_fim]
    )

    # Converte os horários de agendamentos em um conjunto
    agendamentos_horarios = {localtime(agendamento.data_e_hora).replace(second=0, microsecond=0) for agendamento in agendamentos}

    hora_atual = now()  # Usa o horário atual com o fuso horário correto
    limite_minimo_horario = hora_atual + timedelta(hours=2)

    horarios_disponiveis = []

    # Gera os horários disponíveis
    for horario in horarios_colaborador:
        hora_atual = datetime.combine(data_obj.date(), horario.hora_inicio)
        hora_fim = datetime.combine(data_obj.date(), horario.hora_fim)

        # Torna os horários timezone-aware
        hora_atual = make_aware(hora_atual)
        hora_fim = make_aware(hora_fim)

        while hora_atual < hora_fim:
            if (hora_atual >= limite_minimo_horario) and \
                    hora_atual not in agendamentos_horarios:
                horarios_disponiveis.append(hora_atual)
            hora_atual += timedelta(hours=1)

    return horarios_disponiveis

# Rota para obter os horários disponíveis para o colaborador em uma data específica
def horarios_disponiveis(request, colaborador_id):
    data = request.GET.get('data')  # Recebe a data no formato "YYYY-MM-DD"
    if not data:
        return JsonResponse({"error": "O parâmetro 'data' é obrigatório"}, status=400)

    try:
        # Converte a data recebida em um objeto datetime timezone-aware
        data_obj = make_aware(datetime.strptime(data, "%Y-%m-%d"))

        # Obtém os horários disponíveis para o colaborador
        horarios = obter_horarios_disponiveis(colaborador_id, data_obj)

        if horarios:
            return JsonResponse({"horarios_disponiveis": [hora.strftime("%H:%M") for hora in horarios]}, status=200)
        else:
            return JsonResponse({"message": "Nenhum horário disponível."}, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Erro ao buscar horários disponíveis: {str(e)}"}, status=500)

def visualizar_agendamentos(request):
    user = request.user  # Usuário logado
    agendamentos = Agendamento.objects.select_related(
        'cliente', 'colaborador', 'servico', 'plano', 'colaborador__clinica'
    )
    
    # Filtra os agendamentos com base no papel do usuário
    if hasattr(user, 'colaborador') and user.colaborador.is_admin:
        agendamentos = agendamentos.all()
    elif hasattr(user, 'colaborador'):
        agendamentos = agendamentos.filter(colaborador=user.colaborador)
    elif hasattr(user, 'cliente'):
        agendamentos = agendamentos.filter(cliente=user.cliente)
    else:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    
    # Filtragem por campos
    pesquisa_tipo = request.GET.get('pesquisa_tipo', 'agendamento')
    pesquisa_valor = request.GET.get('pesquisa_valor', '')

    # Se pesquisa_valor for fornecido, filtra por ID do agendamento
    if pesquisa_tipo == 'agendamento' and pesquisa_valor.isdigit():
        agendamentos = agendamentos.filter(id=pesquisa_valor)
    elif pesquisa_tipo == 'cliente':
        agendamentos = agendamentos.filter(cliente__nome__icontains=pesquisa_valor)
    elif pesquisa_tipo == 'colaborador':
        agendamentos = agendamentos.filter(colaborador__nome__icontains=pesquisa_valor)
    elif pesquisa_tipo == 'clinica':
        agendamentos = agendamentos.filter(colaborador__clinica__nome__icontains=pesquisa_valor)

    # Ordenação
    sort_key = request.GET.get('sort_key', 'data_e_hora')
    direction = request.GET.get('direction', 'asc')
    if direction == 'desc':
        sort_key = f'-{sort_key}'
    agendamentos = agendamentos.order_by(sort_key)

    # Paginação
    paginator = Paginator(agendamentos, 9)  # 9 itens por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'agendamentos/visualizar_agendamentos.html', {
        'page_obj': page_obj,
        'pesquisa_tipo': pesquisa_tipo,
        'pesquisa_valor': pesquisa_valor,
        'sort_key': sort_key,
        'direction': direction,
    })



def detalhes_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    plano_nome = agendamento.plano.nome if agendamento.plano else 'N/A'

    return render(request, 'agendamentos/detalhes_agendamento.html', {
        'agendamento': agendamento,
        'plano_nome': plano_nome,
    })

def confirmar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    agendamento.status = 'Confirmado'
    agendamento.save()
    return redirect('detalhes_agendamento', agendamento_id=agendamento.id)

def cancelar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    agendamento.status = 'Cancelado'
    agendamento.save()
    return redirect('detalhes_agendamento', agendamento_id=agendamento.id)

def remarcar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    # Verifica o papel (role) do usuário
    role = request.session.get('role', 'desconhecido')

    if role in ['colaborador', 'admin']:
        # Apenas colaboradores e admins podem remarcar diretamente
        agendamento.status = 'Remarcado'
        agendamento.save()
        return redirect('editar_agendamento', agendamento_id)
    elif role == 'cliente':
        # Para clientes, solicita reagendamento e redireciona para os detalhes
        agendamento.status = 'Reagendamento Solicitado'
        agendamento.save()
        return redirect('detalhes_agendamento', agendamento_id)
    else:
        # Caso o usuário não tenha um papel reconhecido
        from django.http import HttpResponseForbidden

        # Retorna uma resposta 403 Forbidden com uma mensagem de erro
        return HttpResponseForbidden("Você não tem permissão para acessar esta funcionalidade.")


@login_required
def excluir_agendamento(request, agendamento_id):
    # Verificar se o usuário tem o papel de colaborador
    if not hasattr(request.user, 'colaborador'):
        messages.error(request, 'Você não tem permissão para excluir agendamentos.')
        return redirect('visualizar_agendamentos')

    try:
        # Buscar o agendamento pelo ID
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)

        # Excluir o agendamento
        agendamento.delete()

        # Adicionar mensagem de sucesso
        messages.success(request, 'Agendamento excluído com sucesso!')

    except Exception as e:
        # Adicionar mensagem de erro em caso de exceção
        messages.error(request, f'Ocorreu um erro ao excluir o agendamento: {str(e)}')

    # Redirecionar para a página de visualização de agendamentos
    return redirect('visualizar_agendamentos')


from django.shortcuts import  get_object_or_404
from .forms import AgendamentoEditForm
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.utils.timezone import localtime
from datetime import datetime

@login_required
def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    
    print(f"DEBUG: Acessando edição do agendamento com ID {agendamento_id}")  # Debug inicial
    print(f"DEBUG: Dados do agendamento: {agendamento}")  # Imprimir a instância do agendamento

    # Quando o formulário for enviado
    if request.method == 'POST':
        print(f"DEBUG: Dados POST recebidos: {request.POST}")  # Imprime os dados enviados no formulário
        form = AgendamentoEditForm(request.POST, instance=agendamento)
        
        if form.is_valid():
            print(f"DEBUG: Formulário válido. Salvando o agendamento...")  # Debug após validação
            form.save()  # Salva as alterações no agendamento
            messages.success(request, 'Agendamento atualizado com sucesso!')
            # Redireciona para a página de visualização de agendamentos com o filtro para o agendamento editado
            return HttpResponseRedirect(f'{reverse("visualizar_agendamentos")}?pesquisa_tipo=agendamento&pesquisa_valor={agendamento.id}')
        else:
            print(f"DEBUG: Formulário inválido. Erros: {form.errors}")  # Erros do formulário
            messages.error(request, 'Erro ao atualizar o agendamento. Verifique os dados e tente novamente.')
    
    # Se a requisição for GET, exibe o formulário com os dados do agendamento
    else:
        # Converte a data para o fuso horário local (Brasília)
        agendamento.data_e_hora = localtime(agendamento.data_e_hora)

        # Formata a data no formato necessário para o campo datetime-local
        formatted_data = agendamento.data_e_hora.strftime('%Y-%m-%dT%H:%M')
        
        # Atualiza o campo de data do formulário com o valor formatado
        form = AgendamentoEditForm(instance=agendamento)
        form.initial['data_e_hora'] = formatted_data
        
        print(f"DEBUG: Carregando formulário para edição com os seguintes dados: {form.initial}")  # Verifica os dados do formulário

    return render(request, 'agendamentos/editar_agendamento.html', {'form': form, 'agendamento': agendamento})
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils.timezone import make_aware
import json

@login_required
def editar_agendamento_dia_horarios(request, agendamento_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)  # Dados do frontend

            # Obter dados da requisição
            nova_data = data.get('data')
            novo_horario = data.get('horario')

            if not nova_data or not novo_horario:
                return JsonResponse({'message': 'Data e horário são obrigatórios.'}, status=400)

            # Buscar o agendamento pelo ID
            agendamento = get_object_or_404(Agendamento, id=agendamento_id)

            # Verificar se o usuário é cliente ou colaborador
            user = request.user
            if hasattr(user, 'cliente') and agendamento.cliente == user.cliente:
                # Solicitar remarcação
                agendamento.status = 'Pedido de Remarcação'
                agendamento.data_e_hora = make_aware(datetime.strptime(f"{nova_data} {novo_horario}", "%Y-%m-%d %H:%M:%S"))
                agendamento.save()

                return JsonResponse({'message': 'Solicitação de remarcação enviada ao administrador.'}, status=200)

            elif hasattr(user, 'colaborador') and (agendamento.colaborador == user.colaborador or user.colaborador.is_admin):
                # Atualizar o dia e horário diretamente
                nova_data_horario = make_aware(datetime.strptime(f"{nova_data} {novo_horario}", "%Y-%m-%d %H:%M:%S"))

                # Verificar conflitos de horário
                conflito = Agendamento.objects.filter(
                    colaborador=agendamento.colaborador,
                    data_e_hora=nova_data_horario
                ).exclude(id=agendamento_id).exists()

                if conflito:
                    return JsonResponse({'message': 'Já existe um agendamento para este colaborador no horário especificado.'}, status=400)

                agendamento.data_e_hora = nova_data_horario
                agendamento.status = 'Confirmado'
                agendamento.save()

                return JsonResponse({'message': 'Dia e horário do agendamento atualizados com sucesso.'}, status=200)

            else:
                return JsonResponse({'message': 'Usuário não autorizado a editar este agendamento.'}, status=403)

        except Exception as e:
            return JsonResponse({'message': f'Erro interno no servidor: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Método não permitido.'}, status=405)

from django.http import JsonResponse

def listar_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    eventos = [
        {
            "id": agendamento.id,
            "title": f"{agendamento.servico.nome_servico} - {agendamento.data_e_hora.strftime('%H:%M')}",
            "start": agendamento.data_e_hora.strftime('%Y-%m-%dT%H:%M:%S'),
            "extendedProps": {
                "cliente": agendamento.cliente.nome if agendamento.cliente else 'Cliente não informado',
                "colaborador": agendamento.colaborador.nome if agendamento.colaborador else 'Colaborador não informado',
                "status": agendamento.status,
            },
            "backgroundColor": get_cor_por_status(agendamento.status),
            "textColor": 'white'  # Cor do texto pode ser ajustada conforme necessário
        }
        for agendamento in agendamentos
    ]
    return JsonResponse(eventos, safe=False)

def get_cor_por_status(status):
    status = status.lower()  # Transforma o status para minúsculas para ignorar maiúsculas e minúsculas
    if status == 'confirmado':
        return '#2ba89a'  # Confirmado: verde
    elif status == 'pendente':
        return 'orange'  # Pendente: laranja
    elif status == 'cancelado':
        return 'red'  # Cancelado: vermelho
    elif status == 'remarcado':
        return 'blue'  # Remarcado: azul
    else:
        return 'gray'  # Cor padrão para status desconhecidos







from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def calendario_agendamentos(request):
    # Obtém o papel do usuário
    role = request.session.get('role', 'desconhecido')
    
    # Filtra os agendamentos com base no papel do usuário
    if role == 'cliente':
        # Cliente só vê seus próprios agendamentos
        agendamentos = Agendamento.objects.filter(cliente=request.user.cliente)
    elif role == 'colaborador':
        # Colaborador só vê seus próprios agendamentos
        agendamentos = Agendamento.objects.filter(colaborador=request.user.colaborador)
    elif role == 'admin':
        # Admin vê todos os agendamentos
        agendamentos = Agendamento.objects.all()
    else:
        # Caso o usuário não tenha um papel reconhecido, não mostra nada ou gera um erro
        agendamentos = Agendamento.objects.none()  # Retorna uma queryset vazia
    
    # Retorna o template com os agendamentos filtrados
    return render(request, 'agendamentos/calendario_agendamentos.html', {'agendamentos': agendamentos})

