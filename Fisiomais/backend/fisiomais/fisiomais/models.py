#python manage.py makemigrations
#python manage.py migrate

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

# Modelo: Endereços
class Endereco(models.Model):
    rua = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    # Relacionamentos
    clientes = models.ManyToManyField('Cliente', related_name='enderecos', blank=True)
    colaboradores = models.ManyToManyField('Colaborador', related_name='enderecos', blank=True)
    clinicas = models.ManyToManyField('Clinica', related_name='enderecos', blank=True)

    def __str__(self):
        return f'{self.rua}, {self.numero}'

# Modelo: Clínicas
class Clinica(models.Model):
    cnpj = models.CharField(max_length=18, unique=True)
    nome = models.CharField(max_length=255)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, unique=True)

    # Relacionamentos
    colaboradores = models.ManyToManyField('Colaborador', related_name='clinicas', blank=True)

    def __str__(self):
        return self.nome

# Modelo: Colaboradores
class Colaborador(AbstractBaseUser):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    admin_nivel = models.CharField(max_length=50, null=True, blank=True)
    referencias = models.TextField(null=True, blank=True)
    cargo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    photo = models.ImageField(upload_to='colaboradores/', null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True)
    clinica = models.ForeignKey(Clinica, on_delete=models.SET_NULL, null=True, blank=True)

    # Relacionamentos
    servicos = models.ManyToManyField('Servico', through='ColaboradorServico', related_name='colaboradores')
    horarios = models.ManyToManyField('Horario', related_name='colaboradores')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf']

    def set_password(self, password):
        self.senha = self.make_random_password(password)

    def check_password(self, password):
        return self.password == password

    def get_photo_url(self):
        """Retorna o URL público da foto."""
        if self.photo:
            return self.photo.url
        return None

    def __str__(self):
        return self.nome

# Modelo: Clientes
class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    referencias = models.TextField(null=True, blank=True)
    dt_nasc = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    photo = models.ImageField(upload_to='clientes/', null=True, blank=True)

    # Novos campos para verificação de email
    email_confirmado = models.BooleanField(default=False)
    token_confirmacao = models.CharField(max_length=128, null=True, blank=True)

    # Relacionamentos
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True)

    def set_password(self, password):
        self.senha = self.make_random_password(password)

    def check_password(self, password):
        return self.password == password

    def get_photo_url(self):
        """Retorna o URL público da foto."""
        if self.photo:
            return self.photo.url
        return None

    def __str__(self):
        return self.nome

# Modelo: Serviços
class Servico(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Relacionamentos
    tipo_servicos = models.ManyToManyField('TipoServico', through='ServicoTipoServico', related_name='servicos')

    def set_valor(self, tipo_servico):
        if tipo_servico == "fisioterapia":
            self.valor = 120.00
        elif tipo_servico == "pilates":
            self.valor = None

    def __str__(self):
        return self.nome

# Modelo: Planos
class Plano(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

# Modelo: TipoServico
class TipoServico(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo

# Tabelas Associativas
class ServicoTipoServico(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    tipo_servico = models.ForeignKey(TipoServico, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('servico', 'tipo_servico')

class ColaboradorServico(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('colaborador', 'servico')

# Modelo: Horários
class Horario(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f'{self.dia_semana} - {self.hora_inicio} até {self.hora_fim}'

# Modelo: Agendamentos
class Agendamento(models.Model):
    data_e_hora = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pendente")
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.data_e_hora} - {self.cliente} - {self.servico}'

class BlacklistedToken(models.Model):
    jti = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.jti