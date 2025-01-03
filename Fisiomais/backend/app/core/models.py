from django.db import models
from django.utils import timezone
from usuarios.models import Colaborador, Cliente
# Create your models here.

# Modelo: Serviços
class Servico(models.Model):
    Nome_servico = models.CharField(max_length=255)
    Descricao = models.TextField()
    Valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_servico = models.CharField(max_length=50)  # fisioterapia ou pilates
    planos = models.JSONField(null=True, blank=True)  # Usar JSONField do Django para armazenar planos

    def __str__(self):
        return self.Nome_servico

# Modelo: Relacionamento Colaboradores e Serviços
class ColaboradoresServicos(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='servicos_relacionados')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='colaboradores_relacionados')

# Modelo: Agendamentos
class Agendamento(models.Model):
    data_e_hora = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='agendamentos')
    ID_Plano = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pendente')

    def __str__(self):
        return f'Agendamento {self.id} - {self.status}'

# Modelo: Tokens em Blacklist
class BlacklistedToken(models.Model):
    jti = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.jti
# Modelo: Horários
class Horario(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f'{self.dia_semana} - {self.hora_inicio} até {self.hora_fim}'