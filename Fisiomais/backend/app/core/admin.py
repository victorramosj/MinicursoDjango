from django.contrib import admin
from .models import Horario, Servico, Agendamento, Plano, TipoServico, ColaboradoresServicos

# Personalizando a exibição do modelo TipoServico no admin
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = ('tipo',)
    search_fields = ('tipo',)

admin.site.register(TipoServico, TipoServicoAdmin)

# Personalizando a exibição do modelo Servico no admin
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome_servico', 'tipo_servico', 'valor')
    list_filter = ('tipo_servico',)
    search_fields = ('nome_servico',)

admin.site.register(Servico, ServicoAdmin)

# Personalizando a exibição do modelo Plano no admin
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'servico', 'valor')
    list_filter = ('servico',)
    search_fields = ('nome',)

admin.site.register(Plano, PlanoAdmin)

# Personalizando a exibição do modelo ColaboradoresServicos no admin
class ColaboradoresServicosAdmin(admin.ModelAdmin):
    list_display = ('colaborador', 'servico')
    search_fields = ('colaborador__nome', 'servico__nome_servico')

admin.site.register(ColaboradoresServicos, ColaboradoresServicosAdmin)

# Personalizando a exibição do modelo Agendamento no admin
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'colaborador', 'servico', 'plano', 'status', 'data_e_hora')
    list_filter = ('status', 'servico', 'colaborador')
    search_fields = ('cliente__nome', 'colaborador__nome', 'servico__nome_servico')

admin.site.register(Agendamento, AgendamentoAdmin)

# Personalizando a exibição do modelo Horario no admin
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('colaborador', 'dia_semana', 'hora_inicio', 'hora_fim')
    list_filter = ('colaborador', 'dia_semana')
    search_fields = ('colaborador__nome',)

admin.site.register(Horario, HorarioAdmin)
