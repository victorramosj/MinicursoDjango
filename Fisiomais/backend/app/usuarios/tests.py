#python manage.py test 
#python manage.py test nome_do_app
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from usuarios.models import Cliente, Colaborador, Clinica 
from django.contrib.messages import get_messages

from .forms import ClienteForm, ColaboradorForm 
class UsuarioViewsTestCase(TestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        
        # Criar clínica antes do colaborador
        self.clinica = Clinica.objects.create(nome="Clínica Teste", cnpj="12345678000100", telefone="123456789")

        # Criar usuário para o colaborador
        self.user_colaborador = User.objects.create_user(username="colaborador_teste", password="senha123")
        self.colaborador = Colaborador.objects.create(
            user=self.user_colaborador, nome="Colaborador Teste", clinica=self.clinica  # Inclui a clínica
        )

        # Criar usuário para o cliente
        self.user_cliente = User.objects.create_user(username="cliente_teste", password="senha123")
        self.cliente = Cliente.objects.create(user=self.user_cliente, nome="Cliente Teste")
        
    def test_custom_login_sucesso(self):
        """Testa se o login ocorre com credenciais corretas"""
        response = self.client.post(reverse("login"), {"username": "cliente_teste", "password": "senha123"})
        self.assertEqual(response.status_code, 302)  # Redireciona após login bem-sucedido
        self.assertTrue("_auth_user_id" in self.client.session)
    
  

    def test_custom_login_falha(self):
        """Testa se o login falha com credenciais inválidas"""
        # Tentativa de login com credenciais incorretas
        response = self.client.post(reverse("login"), {"username": "cliente_teste", "password": "senhaerrada"})

        # Verifica se a resposta é a própria página de login com código 200
        self.assertEqual(response.status_code, 200)
        
        # Captura as mensagens de erro do contexto
        messages = list(get_messages(response.wsgi_request))  # Captura as mensagens através do request

        # Verifica se a mensagem de erro "Usuário ou senha incorretos" foi adicionada
        self.assertTrue(any("Usuário ou senha incorretos" in str(m) for m in messages))

    from django.urls import reverse

    def test_custom_logout(self):
        """Testa se o logout funciona corretamente"""
        # Realiza o logout com uma requisição POST
        response = self.client.post(reverse('logout'))

        # Verifica se o status da resposta é 302 (redirecionamento)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')  # Verifica se redireciona para a página inicial
    

    from django.urls import reverse

    def test_cadastrar_cliente(self):
        """Testa o cadastro de um novo cliente"""
        
        # Dados completos para o novo cliente
        data = {
            "username": "novocliente",  # Nome de usuário
            "nome": "Novo Cliente",  # Nome completo
            "sexo": "M",  # Sexo
            "email": "cliente@email.com",  # Email
            "email2": "cliente@email.com",  # Confirmar email
            "senha": "teste123",  # Senha
            "senha2": "teste123",  # Confirmar senha
            "dt_nasc": "1990-01-01",  # Data de nascimento
            "estado": "PE",  # Estado
            "cidade": "Petrolina",  # Cidade
            "telefone": "87999999999",  # Telefone
            "cpf": "10530125005",  # CPF
            "endereco": "Rua Teste, 123",  # Endereço
            "bairro": "Centro",  # Bairro
            "photo": "",  
            "clinica": self.clinica.id,  
        }

        # Realiza o cadastro do cliente
        response = self.client.post(reverse("cadastrar_cliente"), data)

        # Verifique se houve redirecionamento para a página inicial
        self.assertEqual(response.status_code, 302)  # Verifique se o status é 302 (Redirecionamento)
        self.assertRedirects(response, reverse("home"))  # Verifique se o redirecionamento foi para a URL 'home'
        
        # Verifique se o cliente foi salvo no banco de dados
        self.assertTrue(Cliente.objects.filter(nome="Novo Cliente").exists())  # Verifica se o cliente foi salvo corretamente
      
    


from django.test import TestCase
from usuarios.forms import ClienteForm
from django.db import IntegrityError


class ClienteFormTest(TestCase):
    def test_cadastro_cliente_com_erro(self):
        """Testa o cadastro de um novo cliente com todos os dados inválidos"""
        
        # Dados inválidos para todos os campos
        data = {
            
            "nome": "A",  # Nome muito curto (precisa de pelo menos dois nomes)
            "sexo": "",  # Sexo vazio
            "email": "emailinvalido.com",  # E-mail sem '@'
            "email2": "emaildiferente@outro.com",  # E-mail não corresponde ao anterior
            "senha": "123",  # Senha muito curta
            "senha2": "1234",  # Senha não corresponde à anterior
            "dt_nasc": "2025-01-01",  # Data de nascimento no futuro
            "estado": "",  # Estado vazio
            "cidade": "",  # Cidade vazia
            "telefone": "879999999",  # Telefone com número inválido
            "cpf": "123",  # CPF inválido (muito curto)
            "endereco": "",  # Endereço vazio
            "bairro": "",  # Bairro vazio
            "photo": "",  # Foto vazia
            "clinica": "",  # Clínica não fornecida
        }

        # Criação do formulário com dados inválidos
        form = ClienteForm(data)

        # Verifica que o formulário é inválido
        self.assertFalse(form.is_valid())
        
        # Verifica se os erros corretos são gerados        
        self.assertTrue('nome' in form.errors)
        self.assertTrue('sexo' in form.errors)
        self.assertTrue('email' in form.errors)
        self.assertTrue('email2' in form.errors)
        self.assertTrue('senha' in form.errors)
        self.assertTrue('senha2' in form.errors)
        self.assertTrue('dt_nasc' in form.errors)
        self.assertTrue('estado' in form.errors)
        self.assertTrue('cidade' in form.errors)
        self.assertTrue('telefone' in form.errors)
        self.assertTrue('cpf' in form.errors)

        # Verifica que o cliente não foi salvo no banco de dados
        self.assertEqual(Cliente.objects.count(), 0)

from django.test import TestCase
from django.core.exceptions import ValidationError
from .forms import ColaboradorForm
from .models import Colaborador, Clinica
from django.contrib.auth.models import User
from datetime import date

class TesteFormularioColaborador(TestCase):

    def setUp(self):
        # Criação de uma clínica fictícia para associar ao colaborador
        self.clinica = Clinica.objects.create(nome='Clínica Teste', endereco='Rua Teste, 123')

    def test_formulario_valido(self):
        # Dados válidos para o formulário
        dados_formulario = {
            'username': 'colaborador123',
            'nome': 'João Silva',
            'sexo': 'M',
            'email': 'joao.silva@example.com',
            'email2': 'joao.silva@example.com',
            'senha': 'senha1234',
            'senha2': 'senha1234',
            'cpf': '40407937064',
            'clinica': self.clinica,
            'estado': 'PE',
            'cidade': 'Recife',
            'dt_nasc': '1990-01-01',
            'telefone': '11987654321',
            'cargo': 'Fisioterapeuta',
            'endereco': 'Rua Teste, 123',
            'bairro': 'Bairro Teste',
        }

        formulario = ColaboradorForm(data=dados_formulario)

        # Verifica se o formulário é válido, mas primeiro printa os erros se não for
        if not formulario.is_valid():
            print("Erros do formulário:", formulario.errors)  # Exibe os erros do formulário

        self.assertTrue(formulario.is_valid())  # Verifica se o formulário é válido
        colaborador = formulario.save(commit=False)  # Salva sem persistir no banco

        # Verifica se os dados limpos estão corretos
        self.assertEqual(colaborador.user.username, formulario.cleaned_data['username'])
        self.assertEqual(colaborador.user.email, formulario.cleaned_data['email'])
        self.assertEqual(colaborador.cargo, formulario.cleaned_data['cargo'])


        
    def test_email_diferente(self):
        # Dados com emails diferentes para testar a validação de email
        dados_formulario = {
            'username': 'colaborador123',
            'nome': 'João Silva',
            'sexo': 'M',
            'email': 'joao.silva@example.com',
            'email2': 'outro.email@example.com',  # Emails não coincidem
            'senha': 'senha1234',
            'senha2': 'senha1234',
            'cpf': '12345678901',
            'clinica': self.clinica,
            'estado': 'SP',
            'cidade': 'São Paulo',
            'dt_nasc': '1990-01-01',
            'telefone': '11987654321',
            'cargo': 'Fisioterapeuta',
            'endereco': 'Rua Teste, 123',
            'bairro': 'Bairro Teste',
        }

        formulario = ColaboradorForm(data=dados_formulario)
        
        self.assertFalse(formulario.is_valid())  # Formulário inválido
        self.assertIn('email2', formulario.errors)  # Verifica se o erro de email está presente
    
    def test_senhas_diferentes(self):
        # Dados com senhas diferentes para testar a validação de senha
        dados_formulario = {
            'username': 'colaborador123',
            'nome': 'João Silva',
            'sexo': 'M',
            'email': 'joao.silva@example.com',
            'email2': 'joao.silva@example.com',
            'senha': 'senha1234',
            'senha2': 'senha5678',  # Senhas não coincidem
            'cpf': '12345678901',
            'clinica': self.clinica,
            'estado': 'SP',
            'cidade': 'São Paulo',
            'dt_nasc': '1990-01-01',
            'telefone': '11987654321',
            'cargo': 'Fisioterapeuta',
            'endereco': 'Rua Teste, 123',
            'bairro': 'Bairro Teste',
        }

        formulario = ColaboradorForm(data=dados_formulario)
        
        self.assertFalse(formulario.is_valid())  # Formulário inválido
        self.assertIn('senha2', formulario.errors)  # Verifica se o erro de senha está presente

    def test_cpf_invalido(self):
        # CPF inválido para testar a validação de CPF
        dados_formulario = {
            'username': 'colaborador123',
            'nome': 'João Silva',
            'sexo': 'M',
            'email': 'joao.silva@example.com',
            'email2': 'joao.silva@example.com',
            'senha': 'senha1234',
            'senha2': 'senha1234',
            'cpf': '12345678900',  # CPF inválido
            'clinica': self.clinica,
            'estado': 'SP',
            'cidade': 'São Paulo',
            'dt_nasc': '1990-01-01',
            'telefone': '11987654321',
            'cargo': 'Fisioterapeuta',
            'endereco': 'Rua Teste, 123',
            'bairro': 'Bairro Teste',
        }

        formulario = ColaboradorForm(data=dados_formulario)
        
        self.assertFalse(formulario.is_valid())  # Formulário inválido
        self.assertIn('cpf', formulario.errors)  # Verifica se o erro de CPF está presente

    def test_data_nascimento_invalida(self):
        # Data de nascimento no futuro
        dados_formulario = {
            'username': 'colaborador123',
            'nome': 'João Silva',
            'sexo': 'M',
            'email': 'joao.silva@example.com',
            'email2': 'joao.silva@example.com',
            'senha': 'senha1234',
            'senha2': 'senha1234',
            'cpf': '12345678901',
            'clinica': self.clinica,
            'estado': 'SP',
            'cidade': 'São Paulo',
            'dt_nasc': '2025-01-01',  # Data futura
            'telefone': '11987654321',
            'cargo': 'Fisioterapeuta',
            'endereco': 'Rua Teste, 123',
            'bairro': 'Bairro Teste',
        }

        formulario = ColaboradorForm(data=dados_formulario)
        
        self.assertFalse(formulario.is_valid())  # Formulário inválido
        self.assertIn('dt_nasc', formulario.errors)  # Verifica se o erro de data de nascimento está presente

