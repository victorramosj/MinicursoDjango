from django.contrib import admin
from .models import Horario, Servico, Agendamento

admin.site.register(Horario)
admin.site.register(Servico)
admin.site.register(Agendamento)