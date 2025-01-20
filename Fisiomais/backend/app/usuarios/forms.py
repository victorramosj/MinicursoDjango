# usuarios/forms.py
from django import forms
from django import forms
from .models import Cliente, Colaborador, Clinica
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
import requests
from django.forms.widgets import ClearableFileInput


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuário'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
    )


# Função para validar CPF com cálculo do dígito verificador
def validar_cpf(value):
    """Valida o CPF com regras completas, incluindo cálculo do dígito verificador."""
    cpf = re.sub(r'[^0-9]', '', value)  # Remove caracteres não numéricos
    if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido")
    for i in range(9, 11):
        value_sum = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
        digit = ((value_sum * 10) % 11) % 10
        if digit != int(cpf[i]):
            raise ValidationError("CPF inválido")


class ClienteForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Nome de Usuário")
    nome = forms.CharField(max_length=255, required=True, label="Nome")
    sexo = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], required=True, label="Sexo")
    email = forms.EmailField(required=True)
    email2 = forms.EmailField(required=True, label="Confirmar Email")
    senha = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha")
    senha2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar Senha")
    dt_nasc = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Data de Nascimento")
    estado = forms.CharField(
     widget=forms.Select(attrs={'id': 'id_estado_cadastro_colaborador', 'name': 'estado'}),
     required=True, 
     label="Estado"
    )
    cidade = forms.CharField(
     widget=forms.Select(attrs={'id': 'id_cidade_cadastro_colaborador', 'name': 'cidade'}),
     required=True, 
     label="Cidade"
    )
    

    class Meta:
        model = Cliente
        fields = [
            'nome', 'sexo', 'telefone', 'dt_nasc', 'endereco', 'estado', 'cidade',
            'bairro', 'cpf', 'photo', 'clinica'
        ]

    

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Já existe um usuário com este nome de usuário.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Já existe um usuário com este e-mail.")
        return email

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise ValidationError("Os e-mails não coincidem.")
        return email2

    def clean_senha2(self):
        senha = self.cleaned_data.get('senha')
        senha2 = self.cleaned_data.get('senha2')
        if senha != senha2:
            raise ValidationError("As senhas não coincidem.")
        return senha2
    
    def save(self, commit=True):
        try:
            # Criação do usuário
            user_data = {
                'username': self.cleaned_data['username'],
                'email': self.cleaned_data['email'],
                'password': self.cleaned_data['senha'],
            }
            user = User.objects.create_user(**user_data)

            # Criação do cliente diretamente
            cliente = Cliente.objects.create(
                user=user,
                nome=self.cleaned_data.get('nome'),
                sexo=self.cleaned_data.get('sexo'),
                dt_nasc=self.cleaned_data.get('dt_nasc'),
                estado=self.cleaned_data.get('estado'),
                cidade=self.cleaned_data.get('cidade'),
                cpf=self.cleaned_data.get('cpf'),
                telefone=self.cleaned_data.get('telefone'),
                endereco=self.cleaned_data.get('endereco'),
                bairro=self.cleaned_data.get('bairro'),
                photo=self.cleaned_data.get('photo'),
                clinica=self.cleaned_data.get('clinica')
            )

            if commit:
                return cliente

            return cliente

        except Exception as e:
            # Se o usuário foi criado, apague-o para evitar inconsistências
            if user and user.pk:
                user.delete()
            raise




from django import forms
from django.core.exceptions import ValidationError
from .models import Colaborador, Clinica
from django.contrib.auth.models import User

class ColaboradorForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Nome de Usuário")
    nome = forms.CharField(max_length=255, required=True, label="Nome")
    sexo = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], required=True, label="Sexo")
    email = forms.EmailField(required=True)
    email2 = forms.EmailField(required=True, label="Confirmar E-mail")
    senha = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha")
    senha2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar Senha")
    cpf = forms.CharField(validators=[validar_cpf], required=True, label="CPF")
    clinica = forms.ModelChoiceField(queryset=Clinica.objects.all(), required=True, label="Clínica")

    estado = forms.CharField(
     widget=forms.Select(attrs={'id': 'id_estado_cadastro_colaborador', 'name': 'estado'}),
     required=True, 
     label="Estado"
    )
    cidade = forms.CharField(
     widget=forms.Select(attrs={'id': 'id_cidade_cadastro_colaborador', 'name': 'cidade'}),
     required=True, 
     label="Cidade"
    )

    dt_nasc = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data de Nascimento"
    )

    class Meta:
        model = Colaborador
        fields = [
            'username', 'nome', 'sexo', 'email', 'email2', 'senha', 'senha2', 
            'cpf', 'clinica', 'estado', 'cidade', 'telefone', 'cargo', 'endereco', 
            'bairro', 'dt_nasc'
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Já existe um usuário com este nome de usuário.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Já existe um usuário com este e-mail.")
        return email

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise ValidationError("Os e-mails não coincidem.")
        return email2

    def clean_senha2(self):
        senha = self.cleaned_data.get('senha')
        senha2 = self.cleaned_data.get('senha2')
        if senha != senha2:
            raise ValidationError("As senhas não coincidem.")
        return senha2

    def save(self, commit=True):
        try:
            print("Chamando save do ColaboradorForm")

            # Criação do usuário
            user_data = {
                'username': self.cleaned_data['username'],
                'email': self.cleaned_data['email'],
                'password': self.cleaned_data['senha'],
            }
            user = User.objects.create_user(**user_data)

            # Criação do colaborador diretamente
            colaborador = Colaborador.objects.create(
                user=user,
                nome=self.cleaned_data.get('nome'),
                sexo=self.cleaned_data.get('sexo'),
                telefone=self.cleaned_data.get('telefone'),
                cargo=self.cleaned_data.get('cargo'),
                endereco=self.cleaned_data.get('endereco'),
                estado=self.cleaned_data.get('estado'),
                cidade=self.cleaned_data.get('cidade'),
                bairro=self.cleaned_data.get('bairro'),
                cpf=self.cleaned_data.get('cpf'),
                clinica=self.cleaned_data.get('clinica'),
                dt_nasc=self.cleaned_data.get('dt_nasc')
            )

            if commit:
                print(f"Colaborador salvo: {colaborador.nome}, relacionado a {user.username}")

            return colaborador

        except Exception as e:
            print(f"Erro ao salvar colaborador: {e}")
            # Se o usuário foi criado, apague-o para evitar inconsistências
            if user and user.pk:
                user.delete()
            raise





from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Colaborador, Cliente

class EditarColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'sexo', 'dt_nasc', 'telefone', 'cargo', 'endereco', 'cpf', 'estado', 'cidade', 'bairro', 'photo', 'clinica']

    widgets = {
        'photo': forms.ClearableFileInput(attrs={'class': 'd-none', 'id': 'id_photo'})  # Ocultando o campo de file input
    }

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if Colaborador.objects.filter(telefone=telefone).exclude(id=self.instance.id).exists():
            raise ValidationError("Este número de telefone já está cadastrado para outro colaborador.")
        return telefone

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if Colaborador.objects.filter(cpf=cpf).exclude(id=self.instance.id).exists():
            raise ValidationError("Este CPF já está cadastrado para outro colaborador.")
        return cpf

    def clean_user(self):
        user = self.cleaned_data['user']
        if User.objects.filter(username=user.username).exclude(id=self.instance.user.id).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return user
    


class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'sexo', 'dt_nasc', 'telefone', 'endereco', 'cpf', 'estado', 'cidade', 'bairro', 'photo', 'clinica']

    widgets = {
            'photo': forms.FileInput(attrs={'id': 'id_photo'}), # Apenas FileInput
        }

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if Cliente.objects.filter(telefone=telefone).exclude(id=self.instance.id).exists():
            raise ValidationError("Este número de telefone já está cadastrado para outro cliente.")
        return telefone

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if Cliente.objects.filter(cpf=cpf).exclude(id=self.instance.id).exists():
            raise ValidationError("Este CPF já está cadastrado para outro cliente.")
        return cpf

    def clean_user(self):
        user = self.cleaned_data['user']
        if User.objects.filter(username=user.username).exclude(id=self.instance.user.id).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return user
