from django.db import models
from django.utils import timezone
from usuarios.models import Colaborador, Cliente

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


# Modelo: Horários
class Horario(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f'{self.dia_semana} - {self.hora_inicio} até {self.hora_fim}'
    
#codigos em sql

""" Modelo: Servico 
Criar
INSERT INTO servico (Nome_servico, Descricao, Valor, tipo_servico, planos)
VALUES ('Fisioterapia', 'Tratamento para reabilitação de lesões', 100.00, 'fisioterapia', '{"plano1": "30 sessões", "plano2": "50 sessões"}');

Ler
SELECT * FROM servico WHERE Nome_servico = 'Fisioterapia';

Atualizar
UPDATE servico
SET Valor = 120.00
WHERE Nome_servico = 'Fisioterapia';

Deletar
DELETE FROM servico WHERE Nome_servico = 'Fisioterapia';


"""

""" Modelo: ColaboradoresServicos
Criar
INSERT INTO colaboradoresservicos (colaborador_id, servico_id)
VALUES (1, 2);  

Ler
SELECT * FROM colaboradoresservicos WHERE colaborador_id = 1;


Atualizar
UPDATE colaboradoresservicos
SET servico_id = 3
WHERE colaborador_id = 1 AND servico_id = 2;


Deletar
DELETE FROM colaboradoresservicos WHERE colaborador_id = 1 AND servico_id = 2;



"""

""" Modelo: Agendamento
Criar
INSERT INTO agendamento (data_e_hora, cliente_id, colaborador_id, servico_id, ID_Plano, status)
VALUES ('2025-01-10 14:30:00', 1, 2, 3, 1, 'pendente');
  

Ler
SELECT * FROM agendamento WHERE cliente_id = 1 AND status = 'pendente';



Atualizar
UPDATE agendamento
SET status = 'confirmado'
WHERE id = 1;



Deletar
DELETE FROM agendamento WHERE id = 1;



"""

""" Modelo: horario
Criar
INSERT INTO horario (colaborador_id, dia_semana, hora_inicio, hora_fim)
VALUES (1, 'Segunda-feira', '08:00:00', '12:00:00');

  

Ler
SELECT * FROM horario WHERE colaborador_id = 1 AND dia_semana = 'Segunda-feira';



Atualizar
UPDATE horario
SET hora_inicio = '09:00:00', hora_fim = '13:00:00'
WHERE colaborador_id = 1 AND dia_semana = 'Segunda-feira';




Deletar
DELETE FROM horario WHERE colaborador_id = 1 AND dia_semana = 'Segunda-feira';




"""