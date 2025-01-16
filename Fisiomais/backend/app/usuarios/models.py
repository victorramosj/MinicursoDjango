from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import re


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


# Modelo: Clínica
class Clinica(models.Model):
    # Relacionamento de um para muitos com Colaboradores e Clientes
    cnpj = models.CharField(max_length=18, unique=True)  
    nome = models.CharField(max_length=150, null=True, blank=True)
    telefone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nome

    def numero_colaboradores(self):
        """Retorna o número de colaboradores associados à clínica."""
        return self.colaboradores.count()


# Modelo: Colaborador
class Colaborador(models.Model):
    # Relacionamento de um para um com User
    # Relacionamento de muitos para um com Clinica
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionamento com o modelo User
    nome = models.CharField(max_length=150, null=True, blank=True)
    sexo = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')],
        null=True,
        blank=True
    )  # Sexo do cliente
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    cargo = models.CharField(max_length=100)  # Cargo do colaborador
    endereco = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, validators=[validar_cpf])
    estado = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='colaboradores/photos/', null=True, blank=True)
    clinica = models.ForeignKey(
        Clinica,
        on_delete=models.CASCADE,  # Se a clínica for excluída, o colaborador também será excluído
        related_name='colaboradores',  # Permite acessar os colaboradores a partir da clínica
    )

    def __str__(self):
        return f"{self.user.username} - {self.cargo}"

    @property
    def is_admin(self):
        """Verifica se o colaborador é administrador."""
        return self.user.is_staff or self.user.is_superuser

    @property
    def role(self):
        """Retorna o role do usuário (colaborador)."""
        return "colaborador" if not self.is_admin else "admin"


# Modelo: Cliente
class Cliente(models.Model):
    # Relacionamento de um para um com User
    # Relacionamento de muitos para um com Clinica
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionamento com o modelo User
    nome = models.CharField(max_length=150, null=True, blank=True)
    sexo = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')],
        null=True,
        blank=True
    )  # Sexo do cliente
    telefone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    dt_nasc = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, validators=[validar_cpf])
    photo = models.ImageField(upload_to='clientes/photos/', null=True, blank=True)
    clinica = models.ForeignKey(
        Clinica,
        on_delete=models.SET_NULL,  # Permite que o cliente continue existindo mesmo se a clínica for excluída
        null=True,
        blank=True,
        related_name='clientes',  # Permite acessar os clientes a partir da clínica
    )

    def __str__(self):
        return f"{self.user.username} - Cliente"
    @property
    def role(self):
        """Retorna o role do usuário (cliente)."""
        return "cliente"

