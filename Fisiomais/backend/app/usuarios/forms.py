# usuarios/forms.py
from django import forms
from django import forms
from .models import Cliente, Colaborador, Clinica
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

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
    email = forms.EmailField(required=True)
    email2 = forms.EmailField(required=True, label="Confirmar Email")
    senha = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha")
    senha2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar Senha")

    class Meta:
        model = Cliente
        fields = [
            'telefone', 'dt_nasc', 'endereco', 'estado', 'cidade',
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
        # Salva os dados de User e Cliente
        user_data = {
            'username': self.cleaned_data['username'],
            'email': self.cleaned_data['email'],
            'password': self.cleaned_data['senha'],
        }
        user = User.objects.create_user(**user_data)
        cliente = super().save(commit=False)
        cliente.user = user  # Associa o Cliente ao novo User
        if commit:
            user.save()
            cliente.save()
        return cliente


class ColaboradorForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Nome de Usuário")
    email = forms.EmailField(required=True)

    class Meta:
        model = Colaborador
        fields = [
            'telefone', 'cargo', 'endereco', 'estado', 'cidade',
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

    def save(self, commit=True):
        # Salva os dados de User e Colaborador
        user_data = {
            'username': self.cleaned_data['username'],
            'email': self.cleaned_data['email'],
        }
        user = User.objects.create_user(**user_data)
        colaborador = super().save(commit=False)
        colaborador.user = user  # Associa o Colaborador ao novo User
        if commit:
            user.save()
            colaborador.save()
        return colaborador
