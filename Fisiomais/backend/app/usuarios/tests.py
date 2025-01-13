from django.test import TestCase
from usuarios.models import Cliente, User
from usuarios.forms import ClienteForm

class ClienteFormTest(TestCase):
    def test_cliente_form_valid(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'email2': 'test@example.com',
            'senha': 'password123',
            'senha2': 'password123',
            'nome': 'Test User',
            'sexo': 'M',
            'estado': 'PI',
            'cidade': 'Some City',
            'dt_nasc': '1990-01-01',
            'cpf': '71956683046',  # CPF válido
            'telefone': '86999999999',
            'endereco': 'Rua Exemplo, 123',
            'bairro': 'Bairro Exemplo',
            'clinica': None  # Ajuste caso clinica seja obrigatória
        }

        form = ClienteForm(data)
        if form.is_valid():
            try:
                cliente = form.save()
                self.assertIsNotNone(cliente.pk, "Cliente não foi salvo no banco de dados")
                print(f"Cliente salvo com sucesso: {cliente.nome}, relacionado a {cliente.user.username}")
            except Exception as e:
                print(f"Erro ao salvar cliente no banco: {e}")
                self.fail(f"Exceção ao salvar cliente: {e}")
        else:
            print("Erros no formulário:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"- {field}: {error}")
            self.fail("Formulário inválido")

    def test_cliente_form_invalid(self):
        # Teste com dados inválidos (exemplo: CPF duplicado ou campos obrigatórios faltando)
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'email2': 'diferente@example.com',  # Emails diferentes
            'senha': 'password123',
            'senha2': 'password1234',  # Senhas diferentes
            'nome': 'Test User',
            'sexo': 'M',
            'estado': 'PI',
            'cidade': 'Some City',
            'dt_nasc': '1990-01-01',
            'cpf': '',  # CPF ausente
            'telefone': '',
            'endereco': '',
            'bairro': '',
            'clinica': None
        }

        form = ClienteForm(data)
        self.assertFalse(form.is_valid(), "Formulário deveria ser inválido com dados errados")
        print("Erros esperados no formulário:")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"- {field}: {error}")
