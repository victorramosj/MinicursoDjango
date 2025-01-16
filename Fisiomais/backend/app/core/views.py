
from .models import Agendamento, Plano
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import logging
from .models import Agendamento, Cliente, Colaborador, Servico
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages  # Para exibir mensagens no redirecionamento



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

            # Buscar objetos relacionados
            try:
                cliente = Cliente.objects.get(id=cliente_id)
            except Cliente.DoesNotExist:
                print("Cliente não encontrado:", cliente_id)
                return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

            try:
                colaborador = Colaborador.objects.get(id=colaborador_id)
            except Colaborador.DoesNotExist:
                print("Colaborador não encontrado:", colaborador_id)
                return JsonResponse({'error': 'Colaborador não encontrado'}, status=404)

            try:
                servico = Servico.objects.get(id=servico_id)
            except Servico.DoesNotExist:
                print("Serviço não encontrado:", servico_id)
                return JsonResponse({'error': 'Serviço não encontrado'}, status=404)

            plano = None if not plano_id else Plano.objects.get(id=plano_id)

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
            return redirect('visualizar_agendamentos')
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
from core.models import Horario, Agendamento  # Ajuste o import conforme necessário

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
    agendamentos = Agendamento.objects.select_related(
        'cliente', 'colaborador', 'servico', 'plano', 'colaborador__clinica'
    ).all()

    # Filtragem por campos
    pesquisa_tipo = request.GET.get('pesquisa_tipo', 'agendamento')
    pesquisa_valor = request.GET.get('pesquisa_valor', '')

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
    agendamento.status = 'Remarcado'    
    agendamento.save()
    return redirect('detalhes_agendamento', agendamento_id=agendamento.id)
