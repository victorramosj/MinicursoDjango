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

from datetime import date
class ClienteForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Nome de Usuário")
    nome = forms.CharField(max_length=255, required=True, label="Nome Completo")
    sexo = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], required=True, label="Sexo")
    email = forms.EmailField(required=True)
    email2 = forms.EmailField(required=True, label="Confirmar Email")
    senha = forms.CharField(
        widget=forms.PasswordInput, 
        required=True, 
        label="Senha", 
        min_length=8,  # Validação de comprimento mínimo para a senha
    )    
    senha2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar Senha")   
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
    dt_nasc = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Data de Nascimento")
    
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

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome.split()) < 2:
            raise ValidationError("O nome completo deve incluir pelo menos dois nomes (primeiro e último).")
        return nome
    def clean_dt_nasc(self):
        dt_nasc = self.cleaned_data.get('dt_nasc')
        
        # Verifica se a data de nascimento não é no futuro
        if dt_nasc > date.today():
            raise ValidationError("A data de nascimento não pode ser no futuro.")
        
        # Definindo a idade mínima (18 anos)
        idade_minima = 18
        hoje = date.today()
        idade = hoje.year - dt_nasc.year - ((hoje.month, hoje.day) < (dt_nasc.month, dt_nasc.day))
        
        # Verifica se a pessoa tem a idade mínima
        if idade < idade_minima:
            raise ValidationError(f"A idade mínima para cadastro é de {idade_minima} anos.")
        
        return dt_nasc
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        # Valida o formato do telefone (11 dígitos para Brasil, por exemplo)
        if not re.match(r'^\d{11}$', telefone):
            raise ValidationError("O número de telefone deve ter 11 dígitos.")
        
        return telefone
    

    def save(self, commit=True):
        try:
            nome_completo = self.cleaned_data.get('nome')
        
            # Verifica se o nome completo é válido
            if not nome_completo:
                raise ValidationError("O nome completo é obrigatório.")
            first_name, *middle_names, last_name = nome_completo.split()
            
            user_data = {
                'username': self.cleaned_data['username'],
                'email': self.cleaned_data['email'],
                'password': self.cleaned_data['senha'],
                'first_name': first_name,
                'last_name': last_name
            }
            user = User.objects.create_user(**user_data)

            cliente = Cliente.objects.create(
                user=user,
                nome=nome_completo,
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
    senha = forms.CharField(
        widget=forms.PasswordInput, 
        required=True, 
        label="Senha", 
        min_length=8,  # Validação de comprimento mínimo para a senha
    )
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
    def clean_dt_nasc(self):
        dt_nasc = self.cleaned_data.get('dt_nasc')
        
        # Verifica se a data de nascimento não é no futuro
        if dt_nasc > date.today():
            raise ValidationError("A data de nascimento não pode ser no futuro.")
        
        # Definindo a idade mínima (18 anos)
        idade_minima = 18
        hoje = date.today()
        idade = hoje.year - dt_nasc.year - ((hoje.month, hoje.day) < (dt_nasc.month, dt_nasc.day))
        
        # Verifica se a pessoa tem a idade mínima
        if idade < idade_minima:
            raise ValidationError(f"A idade mínima para cadastro é de {idade_minima} anos.")
        
        return dt_nasc
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        # Valida o formato do telefone (11 dígitos para Brasil, por exemplo)
        if not re.match(r'^\d{11}$', telefone):
            raise ValidationError("O número de telefone deve ter 11 dígitos.")
        
        return telefone
    

    def save(self, commit=True):
        try:
            print("Chamando save do ColaboradorForm")

            nome_completo = self.cleaned_data.get('nome')
        
            # Verifica se o nome completo é válido
            if not nome_completo:
                raise ValidationError("O nome completo é obrigatório.")
            first_name, *middle_names, last_name = nome_completo.split()
            
            user_data = {
                'username': self.cleaned_data['username'],
                'email': self.cleaned_data['email'],
                'password': self.cleaned_data['senha'],
                'first_name': first_name,
                'last_name': last_name
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
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Cliente, Colaborador


class EditarColaboradorForm(forms.ModelForm):
    username = forms.CharField(label="Nome de usuário", max_length=150, required=True)
    email = forms.EmailField(label="E-mail", required=True)
    senha_atual = forms.CharField(label="Senha atual", widget=forms.PasswordInput, required=False)
    senha = forms.CharField(label="Nova senha", widget=forms.PasswordInput, required=False)
    confirmar_senha = forms.CharField(label="Confirmar nova senha", widget=forms.PasswordInput, required=False)

    class Meta:
        model = Colaborador
        fields = [
            'nome', 'sexo', 'dt_nasc', 'telefone', 'cargo', 'endereco', 'cpf', 'estado', 
            'cidade', 'bairro', 'photo', 'clinica', 'username', 'email', 'senha', 'confirmar_senha'
        ]

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if user_instance:
            self.fields['username'].initial = user_instance.username
            self.fields['email'].initial = user_instance.email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha_atual = cleaned_data.get('senha_atual')
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        # Valida a senha atual se uma nova senha for fornecida
        if senha:
            if not senha_atual:
                raise ValidationError("A senha atual é necessária para alterar a senha.")
            if not self.user_instance.check_password(senha_atual):
                raise ValidationError("A senha atual está incorreta.")
            if senha != confirmar_senha:
                raise ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = instance.user

        # Separar primeiro e último nome
        nome_completo = self.cleaned_data.get('nome', "").strip()
        nome_partes = nome_completo.split()

        user.first_name = nome_partes[0] if nome_partes else ""
        user.last_name = nome_partes[1] if len(nome_partes) > 1 else ""

        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        senha = self.cleaned_data.get('senha')
        if senha:
            user.set_password(senha)

        if commit:
            user.save()
            instance.save()
        return instance



class EditarClienteForm(forms.ModelForm):
    username = forms.CharField(label="Nome de usuário", max_length=150, required=True)
    email = forms.EmailField(label="E-mail", required=True)
    senha_atual = forms.CharField(label="Senha atual", widget=forms.PasswordInput, required=False)
    senha = forms.CharField(
        widget=forms.PasswordInput, 
        required=True, 
        label="Senha", 
        min_length=8,  # Validação de comprimento mínimo para a senha
    )
    confirmar_senha = forms.CharField(label="Confirmar nova senha", widget=forms.PasswordInput, required=False)


    class Meta:
        model = Cliente
        fields = [
            'nome', 'sexo', 'dt_nasc', 'telefone', 'endereco', 'cpf', 'estado', 'cidade', 
            'bairro', 'photo', 'clinica', 'username', 'email', 'senha', 'confirmar_senha'
        ]

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)  # Salva o valor em um atributo
        super().__init__(*args, **kwargs)
        if self.user_instance:
            self.fields['username'].initial = self.user_instance.username
            self.fields['email'].initial = self.user_instance.email


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha_atual = cleaned_data.get('senha_atual')
        senha = forms.CharField(
        widget=forms.PasswordInput, 
        required=True, 
        label="Senha", 
        min_length=8,  # Validação de comprimento mínimo para a senha
    )
        confirmar_senha = cleaned_data.get('confirmar_senha')

        # Valida a senha atual se uma nova senha for fornecida
        if senha:
            if not senha_atual:
                raise ValidationError("A senha atual é necessária para alterar a senha.")
            if not self.user_instance.check_password(senha_atual):  # Agora funciona corretamente
                raise ValidationError("A senha atual está incorreta.")
            if senha != confirmar_senha:
                raise ValidationError("As senhas não coincidem.")
        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        user = instance.user

        # Separar primeiro e último nome
        nome_completo = self.cleaned_data.get('nome', "").strip()
        nome_partes = nome_completo.split()

        user.first_name = nome_partes[0] if nome_partes else ""
        user.last_name = nome_partes[1] if len(nome_partes) > 1 else ""

        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        senha = self.cleaned_data.get('senha')
        if senha:
            user.set_password(senha)

        if commit:
            user.save()
            instance.save()
        return instance

