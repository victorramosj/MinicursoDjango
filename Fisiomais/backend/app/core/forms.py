
from django import forms
from datetime import datetime
from .models import Agendamento, Cliente, Servico, Plano, Colaborador
from django.utils.timezone import localtime, is_naive, make_aware

class AgendamentoEditForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data_e_hora', 'cliente', 'colaborador', 'servico', 'plano', 'status', 'status_pagamento']
        widgets = {
            'data_e_hora': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Selecione a data e hora',
                'min': datetime.now().strftime('%Y-%m-%dT%H:%M')  # Define a data mínima para o campo datetime-local
            }),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('pendente', 'Pendente'),
                ('confirmado', 'Confirmado'),
                ('finalizado', 'Finalizado'),
                ('remarcado', 'Remarcado'),
            ]),
            'status_pagamento': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('pendente', 'Pendente'),
                ('pago', 'Pago'),
            ]),
            'cliente': forms.Select(attrs={'class': 'form-control'})  # Campo de seleção de cliente
        }

    def __init__(self, *args, **kwargs):
        super(AgendamentoEditForm, self).__init__(*args, **kwargs)

        # Inicializa os campos 'cliente', 'serviço' e 'plano'
        self.fields['cliente'].queryset = Cliente.objects.all()  # Exibe todos os clientes
        self.fields['servico'].queryset = Servico.objects.all()
        self.fields['plano'].queryset = Plano.objects.all()

        # Se o cliente for selecionado (ao editar o agendamento)
        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                cliente = Cliente.objects.get(id=cliente_id)
                # Verifica se o cliente tem clínica associada
                if cliente.clinica:
                    self.fields['colaborador'].queryset = Colaborador.objects.filter(clinica=cliente.clinica)
                    # Se o colaborador atual não estiver na lista de colaboradores válidos, redefinir o valor
                    if self.instance.colaborador and self.instance.colaborador not in self.fields['colaborador'].queryset:
                        self.instance.colaborador = None
                else:
                    # Se o cliente não tem clínica associada, não mostra colaboradores
                    self.fields['colaborador'].queryset = Colaborador.objects.none()
            except (ValueError, Cliente.DoesNotExist):
                self.fields['colaborador'].queryset = Colaborador.objects.none()
        elif self.instance.pk:  # Quando estamos editando um agendamento
            # A clínica do cliente deve ser a mesma do colaborador
            if self.instance.cliente.clinica:
                self.fields['colaborador'].queryset = Colaborador.objects.filter(clinica=self.instance.cliente.clinica)
            else:
                self.fields['colaborador'].queryset = Colaborador.objects.none()

            # Define o valor inicial do colaborador com base no colaborador do agendamento
            self.fields['colaborador'].initial = self.instance.colaborador

        # Define os valores iniciais para status e status_pagamento
        if self.instance.pk:
            self.fields['status'].initial = self.instance.status
            self.fields['status_pagamento'].initial = self.instance.status_pagamento

            # Aqui, ajusta-se para garantir que o campo data_e_hora seja formatado corretamente.
            if self.instance.data_e_hora:
                aware_data = self.instance.data_e_hora
                if is_naive(aware_data):
                    aware_data = make_aware(aware_data)  # Converte para aware, caso necessário

                # Converte a data UTC para o fuso horário local (Brasília)
                aware_data = localtime(aware_data)

                # Agora formata a data e hora para o formato necessário para o campo datetime-local
                self.fields['data_e_hora'].initial = aware_data.strftime('%Y-%m-%dT%H:%M')

    # Validação de data e hora
    def clean(self):
        cleaned_data = super().clean()
        data_e_hora = cleaned_data.get('data_e_hora')

        if data_e_hora:
            # Verifica se a data/hora é naive e converte para aware
            if is_naive(data_e_hora):
                data_e_hora = make_aware(data_e_hora)

            # Compara com o datetime atual também em formato aware
            agora = make_aware(datetime.now())
            if data_e_hora < agora:
                raise forms.ValidationError("A data e hora não podem estar no passado.")

            cleaned_data['data_e_hora'] = data_e_hora

        return cleaned_data











