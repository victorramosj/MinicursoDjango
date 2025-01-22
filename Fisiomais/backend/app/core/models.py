from django.db import models
from usuarios.models import Colaborador, Cliente, Clinica

# Modelo: TipoServico
class TipoServico(models.Model):
    tipo = models.CharField(max_length=50, unique=True)  # Ex: "fisioterapia" ou "pilates"

    def __str__(self):
        return self.tipo

# Modelo: Serviço
class Servico(models.Model):
    nome_servico = models.CharField(max_length=255)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_servico = models.ForeignKey(TipoServico, on_delete=models.CASCADE, related_name="servicos")

    def __str__(self):
        return self.nome_servico

# Modelo: Plano
class Plano(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name="planos")

    def __str__(self):
        return self.nome

# Modelo: Relacionamento Colaboradores e Serviços
class ColaboradoresServicos(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='servicos_relacionados')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='colaboradores_relacionados')

    class Meta:
        unique_together = ('colaborador', 'servico')

# Modelo: Agendamento
class Agendamento(models.Model):
    data_e_hora = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='agendamentos')
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True, related_name='agendamentos')
    status = models.CharField(max_length=20, default='pendente')
    status_pagamento = models.CharField(max_length=20, default='pendente')

    def __str__(self):
        return f'Agendamento {self.id} - {self.status}'

# Definindo os dias da semana como um ChoiceField
DIA_SEMANA_CHOICES = [
    ('segunda-feira', 'Segunda-feira'),
    ('terca-feira', 'Terça-feira'),
    ('quarta-feira', 'Quarta-feira'),
    ('quinta-feira', 'Quinta-feira'),
    ('sexta-feira', 'Sexta-feira'),
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
]

# Modelo Horário
class Horario(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=20, choices=DIA_SEMANA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f'{self.get_dia_semana_display()} - {self.hora_inicio} até {self.hora_fim}'
