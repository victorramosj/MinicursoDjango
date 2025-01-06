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
#Códigos sql
""" Modelo: Clinica
Criar
INSERT INTO clinica (cnpj, nome, telefone, endereco, estado, cidade, bairro)
VALUES ('12.345.678/0001-90', 'Clínica Exemplo', '1234-5678', 'Rua Exemplo, 123', 'São Paulo', 'São Paulo', 'Bairro Exemplo');

Ler
SELECT * FROM clinica;
SELECT * FROM clinica WHERE cnpj = '12.345.678/0001-90';

Atualizar
UPDATE clinica
SET nome = 'Clínica Atualizada', telefone = '9876-5432', endereco = 'Nova Rua, 456'
WHERE cnpj = '12.345.678/0001-90';

Deletar
DELETE FROM clinica WHERE cnpj = '12.345.678/0001-90';
"""

""" Modelo: Colaborador
Criar
INSERT INTO colaborador (user_id, nome, sexo, telefone, cargo, endereco, cpf, estado, cidade, bairro, photo, clinica_id)
VALUES (1, 'João Silva', 'Masculino', '9876-5432', 'Fisioterapeuta', 'Rua Colaborador, 456', '12345678901', 'São Paulo', 'São Paulo', 'Bairro Colaborador', 'foto.jpg', 1);


Ler
SELECT * FROM colaborador;
SELECT * FROM colaborador WHERE cpf = '12345678901';

Atualizar
UPDATE colaborador
SET telefone = '9999-8888', cargo = 'Pilates Instrutor', sexo = 'Masculino'
WHERE cpf = '12345678901';


Deletar
DELETE FROM colaborador WHERE cpf = '12345678901';
"""

""" Modelo: Cliente
Criar
INSERT INTO cliente (user_id, nome, sexo, telefone, dt_nasc, endereco, estado, cidade, bairro, cpf, photo, clinica_id)
VALUES (2, 'Maria Oliveira', 'Feminino', '9876-1234', '1990-05-10', 'Rua Cliente, 123', 'São Paulo', 'São Paulo', 'Bairro Cliente', '98765432100', 'foto_cliente.jpg', 1);

Ler
SELECT * FROM cliente;
SELECT * FROM cliente WHERE cpf = '98765432100';

Atualizar
UPDATE cliente
SET telefone = '9876-4321', endereco = 'Nova Rua, 789', sexo = 'Feminino'
WHERE cpf = '98765432100';


Deletar
DELETE FROM cliente WHERE cpf = '98765432100';
"""