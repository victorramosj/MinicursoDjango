from django.urls import path
from . import views

urlpatterns = [
    path('agendar/', views.agendar, name='agendar'),  # Rota para agendar
    path('planos/<int:servico_id>/', views.get_planos, name='get_planos'),  # API para buscar planos de um serviço
    path('horarios/<int:colaborador_id>/', views.get_horarios, name='get_horarios'),  # API para buscar horários
    path('dias-permitidos/<int:colaborador_id>/', views.dias_permitidos, name='dias_permitidos'),
    path('horarios-disponiveis/<int:colaborador_id>/', views.horarios_disponiveis, name='horarios_disponiveis'),
    path('get_servicos/', views.get_servicos, name='get_servicos'),  # Rota para agendar
]
