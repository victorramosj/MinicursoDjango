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


# Formulário de Cadastro de Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'telefone',
            'dt_nasc',
            'endereco',
            'estado',
            'cidade',
            'bairro',
            'cpf',
            'photo',
            'clinica',
        ]

    telefone = forms.CharField(max_length=20, required=True)
    dt_nasc = forms.DateField(required=True)
    endereco = forms.CharField(max_length=255, required=False)
    estado = forms.CharField(max_length=50, required=False)
    cidade = forms.CharField(max_length=100, required=False)
    bairro = forms.CharField(max_length=100, required=False)
    cpf = forms.CharField(max_length=11, required=True, validators=[validar_cpf])
    photo = forms.ImageField(required=False)
    clinica = forms.ModelChoiceField(queryset=Clinica.objects.all(), required=False)

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if Cliente.objects.filter(cpf=cpf).exists():
            raise ValidationError("Já existe um cliente com esse CPF.")
        return cpf


# Formulário de Cadastro de Colaborador
class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = [
            'telefone',
            'cargo',
            'endereco',
            'estado',
            'cidade',
            'bairro',
            'cpf',
            'photo',
            'clinica',
        ]

    telefone = forms.CharField(max_length=20, required=True)
    cargo = forms.CharField(max_length=100, required=True)
    endereco = forms.CharField(max_length=255, required=False)
    estado = forms.CharField(max_length=50, required=False)
    cidade = forms.CharField(max_length=100, required=False)
    bairro = forms.CharField(max_length=100, required=False)
    cpf = forms.CharField(max_length=11, required=True, validators=[validar_cpf])
    photo = forms.ImageField(required=False)
    clinica = forms.ModelChoiceField(queryset=Clinica.objects.all(), required=True)

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if Colaborador.objects.filter(cpf=cpf).exists():
            raise ValidationError("Já existe um colaborador com esse CPF.")
        return cpf
