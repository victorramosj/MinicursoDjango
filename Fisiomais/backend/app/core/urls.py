from django.urls import path
from . import views

urlpatterns = [
    path('agendamentos/agendar/', views.agendar, name='agendar'),  # Rota para agendar
    path('planos/<int:servico_id>/', views.get_planos, name='get_planos'),  # API para buscar planos de um serviço
    path('horarios/<int:colaborador_id>/', views.get_horarios, name='get_horarios'),  # API para buscar horários
    path('dias-permitidos/<int:colaborador_id>/', views.dias_permitidos, name='dias_permitidos'),
    path('horarios-disponiveis/<int:colaborador_id>/', views.horarios_disponiveis, name='horarios_disponiveis'),
    path('get_servicos/', views.get_servicos, name='get_servicos'),  # Rota para agendar
    path('agendamentos/', views.visualizar_agendamentos, name='visualizar_agendamentos'),
    path('agendamentos/<int:agendamento_id>/', views.detalhes_agendamento, name='detalhes_agendamento'),
    path('agendamentos/confirmar/<int:agendamento_id>/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('agendamentos/cancelar/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('agendamentos/remarcar/<int:agendamento_id>/', views.remarcar_agendamento, name='remarcar_agendamento'),
    path('excluir_agendamento/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'),
    path('agendamentos/editaragendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),  # Modificado
]
