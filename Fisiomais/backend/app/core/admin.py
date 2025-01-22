from django.contrib import admin
from .models import Horario, Servico, Agendamento, Plano, TipoServico, ColaboradoresServicos

# Personalizando a exibição do modelo TipoServico no admin
@admin.register(TipoServico)
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')
    search_fields = ('tipo',)
    ordering = ('tipo',)

# Personalizando a exibição do modelo Servico no admin
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_servico', 'tipo_servico', 'valor')
    list_filter = ('tipo_servico',)
    search_fields = ('nome_servico', 'descricao')
    ordering = ('nome_servico',)

# Personalizando a exibição do modelo Plano no admin
@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'servico', 'valor')
    list_filter = ('servico',)
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)

# Personalizando a exibição do modelo ColaboradoresServicos no admin
@admin.register(ColaboradoresServicos)
class ColaboradoresServicosAdmin(admin.ModelAdmin):
    list_display = ('id', 'colaborador', 'servico')
    list_filter = ('servico', 'colaborador__clinica')
    search_fields = ('colaborador__nome', 'servico__nome_servico')
    autocomplete_fields = ('colaborador', 'servico')  # Melhor desempenho em grandes bases de dados

# Personalizando a exibição do modelo Agendamento no admin
@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'colaborador', 'servico', 'plano', 'status', 'data_e_hora')
    list_filter = ('status', 'servico', 'colaborador__clinica', 'data_e_hora')
    search_fields = ('cliente__nome', 'colaborador__nome', 'servico__nome_servico')
    date_hierarchy = 'data_e_hora'  # Navegação por datas
    ordering = ('-data_e_hora',)  # Exibir agendamentos mais recentes primeiro
    autocomplete_fields = ('cliente', 'colaborador', 'servico', 'plano')  # Otimização

# Personalizando a exibição do modelo Horario no admin
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'colaborador', 'dia_semana', 'hora_inicio', 'hora_fim')
    list_filter = ('colaborador__clinica', 'dia_semana')
    search_fields = ('colaborador__nome', 'dia_semana')
    ordering = ('dia_semana', 'hora_inicio')
    autocomplete_fields = ('colaborador',)  # Melhor performance para colaboradores

# Melhorias adicionais:
# 1. Adicionado `autocomplete_fields` para campos relacionados a outras tabelas, melhorando o desempenho com grandes quantidades de dados.
# 2. Ordenação padrão configurada em cada modelo (`ordering`).
# 3. `date_hierarchy` no modelo `Agendamento`, permitindo navegação por datas no Django Admin.
# 4. Filtros foram enriquecidos para incluir informações relacionadas (como clínica dos colaboradores e data/hora).
