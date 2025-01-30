from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import Agendamento, Cliente, Colaborador, Servico, Clinica, Plano, TipoServico, Horario

class AgendamentoTestCase(TestCase):    
    def setUp(self):
        """Configuração inicial para os testes"""

        # Criando usuário admin para autenticação
        self.user = User.objects.create_user(username='admin', password='admin123')

        # Criando clínica
        self.clinica = Clinica.objects.create(nome="Clínica Teste", cnpj="12345678000100")

        # Criando colaborador e cliente
        self.colaborador = Colaborador.objects.create(
            user=self.user, nome="Colaborador Teste", telefone="999999999",
            cpf="12345678900", endereco="Rua A, 123", clinica=self.clinica
        )

        self.cliente = Cliente.objects.create(
            user=self.user, nome="Cliente Teste", telefone="999999999",
            cpf="98765432100", endereco="Rua B, 456"
        )

        # Associando tipos de serviço existentes (ID 1 para Fisioterapia e 2 para Pilates)
        self.fisioterapia = TipoServico.objects.get(id=1)
        self.pilates = TipoServico.objects.get(id=2)

        # Criando serviço e associando um tipo de serviço existente
        self.servico = Servico.objects.create(nome_servico="Pilates", tipo_servico=self.pilates)

        # Criando plano com valor
        self.plano = Plano.objects.create(nome="Plano Mensal", servico=self.servico, valor=100.0)

        # Cliente de teste autenticado
        self.client = Client()
        self.client.login(username='admin', password='admin123')

        # Dados básicos do agendamento
        self.valid_data = {
            "cliente": self.cliente.id,
            "colaborador": self.colaborador.id,
            "servico": self.servico.id,
            "plano": self.plano.id,
            "data": (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            "hora": "10:00"
        }


    def test_agendamento_sucesso(self):
        """Teste de agendamento bem-sucedido"""
        response = self.client.post(reverse('agendar'), self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso
        self.assertTrue(Agendamento.objects.exists())

    def test_agendamento_falta_dados(self):
        """Teste de erro ao faltar dados obrigatórios"""
        invalid_data = self.valid_data.copy()
        invalid_data.pop("data")  # Remove a data para simular erro
        response = self.client.post(reverse('agendar'), invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Agendamento.objects.exists())

    def test_cliente_nao_existe(self):
        """Teste de erro ao tentar agendar com um cliente inexistente"""
        invalid_data = self.valid_data.copy()
        invalid_data["cliente"] = 999  # ID inválido
        response = self.client.post(reverse('agendar'), invalid_data)
        self.assertEqual(response.status_code, 404)

    def test_colaborador_nao_existe(self):
        """Teste de erro ao tentar agendar com um colaborador inexistente"""
        invalid_data = self.valid_data.copy()
        invalid_data["colaborador"] = 999  # ID inválido
        response = self.client.post(reverse('agendar'), invalid_data)
        self.assertEqual(response.status_code, 404)

    def test_data_hora_invalida(self):
        """Teste de erro ao enviar data ou hora inválida"""
        invalid_data = self.valid_data.copy()
        invalid_data["data"] = "data_invalida"
        response = self.client.post(reverse('agendar'), invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_cliente_sem_clinica(self):
        """Teste se um cliente sem clínica recebe a clínica do colaborador"""
        self.cliente.clinica = None
        self.cliente.save()

        response = self.client.post(reverse('agendar'), self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso

        # Verifica se a clínica foi atribuída ao cliente
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.clinica, self.colaborador.clinica)


class DiasPermitidosTestCase(TestCase):
    def setUp(self):
        # Cria uma clínica fictícia
        self.clinica = Clinica.objects.create(nome="Clínica Teste", cnpj="12345678000195")

        # Cria um usuário para associar ao colaborador
        user = User.objects.create_user(username="colaborador_teste", password="password123")
        
        # Cria um colaborador
        self.colaborador = Colaborador.objects.create(
            user=user,
            nome="Colaborador Teste",
            telefone="999999999",
            cpf="12345678900",
            endereco="Rua A, 123",
            clinica=self.clinica
        )

        # Verificar se o colaborador tem a clínica associada
        self.assertEqual(self.colaborador.clinica, self.clinica)

        # Cria um horário para o colaborador
        Horario.objects.create(colaborador=self.colaborador, hora_inicio="08:00", hora_fim="12:00", dia_semana="segunda-feira")

    def test_dias_permitidos(self):
        colaborador = Colaborador.objects.first()
        response = self.client.get(reverse('dias_permitidos', args=[colaborador.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("dias_permitidos", response.json())
        self.assertEqual(len(response.json()['dias_permitidos']), 1)

class HorariosDisponiveisTestCase(TestCase):
    def setUp(self):
        # Cria uma clínica fictícia
        self.clinica = Clinica.objects.create(nome="Clínica Teste", cnpj="12345678000195")

        # Cria um usuário para associar ao colaborador
        user = User.objects.create_user(username="colaborador_teste", password="password123")
        
        # Cria um colaborador
        self.colaborador = Colaborador.objects.create(
            user=user,
            nome="Colaborador Teste",
            telefone="999999999",
            cpf="12345678900",
            endereco="Rua A, 123",
            clinica=self.clinica
        )

        # Verificar se o colaborador tem a clínica associada
        self.assertEqual(self.colaborador.clinica, self.clinica)

        # Cria um horário para o colaborador
        Horario.objects.create(colaborador=self.colaborador, hora_inicio="08:00", hora_fim="12:00", dia_semana="segunda-feira")
        
        # Cria um usuário para o cliente e associa o e-mail
        cliente_user = User.objects.create_user(username="cliente_teste", password="password123", email="cliente@teste.com")
        
        # Cria um cliente associando o usuário
        cliente = Cliente.objects.create(
            user=cliente_user,  # Associa o cliente ao usuário com e-mail
            nome="Cliente Teste",
            telefone="9988776655",
            cpf="12345678901",
            endereco="Rua B, 456"
        )

        # Cria o TipoServico (fisioterapia e pilates)
        tipo_pilates = TipoServico.objects.create(tipo="pilates")


        # Cria um serviço fictício com o TipoServico associado
        servico = Servico.objects.create(nome_servico="Serviço Teste", valor=100.0, tipo_servico=tipo_pilates)

        # Cria um agendamento para o colaborador e o cliente, agora com o serviço associado
        Agendamento.objects.create(
            colaborador=self.colaborador,
            cliente=cliente,  # Associando o cliente
            servico=servico,  # Associando o serviço
            data_e_hora=datetime(2025, 1, 30, 9, 0)
        )

    def test_horarios_disponiveis(self):
        colaborador = Colaborador.objects.first()
        response = self.client.get(reverse('horarios_disponiveis', args=[colaborador.id]), {'data': '2025-01-30'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("horarios_disponiveis", response.json())
        self.assertEqual(len(response.json()['horarios_disponiveis']), 2)  # Deve retornar horários disponíveis excluindo 09:00
