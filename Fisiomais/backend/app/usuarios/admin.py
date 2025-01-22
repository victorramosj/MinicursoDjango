from django.contrib import admin
from django.utils.html import format_html
from .models import Clinica, Colaborador, Cliente

# Configuração da interface administrativa para Clinica
@admin.register(Clinica)
class ClinicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone', 'endereco', 'numero_colaboradores', 'numero_clientes')
    search_fields = ('nome', 'cnpj', 'estado', 'cidade', 'bairro')
    list_filter = ('estado', 'cidade', 'bairro')
    ordering = ('nome',)

    def numero_colaboradores(self, obj):
        return obj.colaboradores.count()
    numero_colaboradores.short_description = 'Número de Colaboradores'

    def numero_clientes(self, obj):
        return obj.clientes.count()
    numero_clientes.short_description = 'Número de Clientes'

# Configuração da interface administrativa para Colaborador
@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'cpf', 'telefone', 'email', 'clinica', 'is_admin', 'data_nascimento_formatada')
    search_fields = ('nome', 'cpf', 'cargo', 'telefone', 'user__email', 'clinica__nome')
    list_filter = ('clinica', 'cargo', 'estado', 'cidade')
    ordering = ('nome',)
    readonly_fields = ('is_admin',)

    def email(self, obj):
        return obj.user.email
    email.short_description = 'E-mail'

    def is_admin(self, obj):
        return 'Sim' if obj.user.is_staff or obj.user.is_superuser else 'Não'
    is_admin.short_description = 'Administrador'

    def data_nascimento_formatada(self, obj):
        return obj.dt_nasc.strftime('%d/%m/%Y') if obj.dt_nasc else 'Não informado'
    data_nascimento_formatada.short_description = 'Data de Nascimento'

# Configuração da interface administrativa para Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email', 'clinica', 'data_nascimento_formatada')
    search_fields = ('nome', 'cpf', 'telefone', 'user__email', 'clinica__nome')
    list_filter = ('clinica', 'estado', 'cidade', 'bairro')
    ordering = ('nome',)

    def email(self, obj):
        return obj.user.email
    email.short_description = 'E-mail'

    def data_nascimento_formatada(self, obj):
        return obj.dt_nasc.strftime('%d/%m/%Y') if obj.dt_nasc else 'Não informado'
    data_nascimento_formatada.short_description = 'Data de Nascimento'
