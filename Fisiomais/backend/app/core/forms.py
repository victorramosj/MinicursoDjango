
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, date


from .models import Clinica, Cliente, Servico
from django.core.validators import MinValueValidator

class AgendamentoForm(forms.Form):    
    clinica_id = forms.ModelChoiceField(queryset=Clinica.objects.all(), required=True, label="Clínica", empty_label="Selecione a Clínica")
    cliente_id = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente", empty_label="Selecione o Cliente")
    servico_id = forms.ModelChoiceField(queryset=Servico.objects.all(), required=True, label="Serviço", empty_label="Selecione o Serviço")

    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
        required=True, label="Data", initial=date.today, validators=[MinValueValidator(date.today)]
    )
    
    hora = forms.ChoiceField(choices=[], required=True, label="Hora")
    
    plano = forms.ChoiceField(choices=[], required=False, label="Plano", help_text="Selecione o plano disponível.")
    
    data_e_hora = forms.DateTimeField(
        label="Data e Hora", widget=forms.HiddenInput(), required=False
    )

    def clean_data_e_hora(self):
        """
        Concatena data e hora em um único campo DateTime para o modelo Agendamento.
        """
        data = self.cleaned_data.get('data')
        hora = self.cleaned_data.get('hora')

        if data and hora:
            try:
                # Concatena data e hora, garantindo o formato correto para o campo DateTimeField
                data_hora_str = f"{data} {hora}:00"
                data_e_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
                return data_e_hora
            except ValueError:
                raise ValidationError("A hora fornecida não é válida ou não está disponível.")
        else:
            raise ValidationError("Data ou hora não fornecidas corretamente.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Atualizando as opções de hora e planos
        self.fields['hora'].choices = [
            ('06:00', '06:00'), 
            ('07:00', '07:00'), 
            ('08:00', '08:00'), 
            ('09:00', '09:00'), 
            ('10:00', '10:00'),
            ('11:00', '11:00'),
            ('12:00', '12:00'),
            ('13:00', '13:00'),
            ('14:00', '14:00'),
            ('15:00', '16:00'),
            ('16:00', '16:00'),
            ('17:00', '17:00'),
            ('18:00', '18:00'),
            
        ]
        
        # Adicionando planos conforme os serviços disponíveis
        self.fields['plano'].choices = [
            ('plano1', 'Plano 1'),
            ('plano2', 'Plano 2'),
            
        ]


from django import forms
from .models import Agendamento, Cliente, Colaborador, Servico, Plano
from datetime import datetime

class AgendamentoEditForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data_e_hora', 'cliente', 'colaborador', 'servico', 'plano', 'status', 'status_pagamento']
        widgets = {
            'data_e_hora': forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'placeholder': 'Selecione a data e hora'
        }),
        'status': forms.Select(attrs={'class': 'form-control'}, choices=[
            ('', 'Selecione o status'),
            ('pendente', 'Pendente'),
            ('confirmado', 'Confirmado'),
            ('finalizado', 'Finalizado'),
            ('remarcado', 'Remarcado'),
        ]),
        'status_pagamento': forms.Select(attrs={'class': 'form-control'}, choices=[
            ('', 'Selecione o status de pagamento'),
            ('pendente', 'Pendente'),
            ('pago', 'Pago'),
        ]),
}


    def __init__(self, *args, **kwargs):
        super(AgendamentoEditForm, self).__init__(*args, **kwargs)
        
        # Filtrar os clientes, serviços e planos
        self.fields['cliente'].queryset = Cliente.objects.all()
        self.fields['servico'].queryset = Servico.objects.all()
        self.fields['plano'].queryset = Plano.objects.all()

        # Inicializa o campo colaborador com base na clínica do cliente
        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                cliente = Cliente.objects.get(id=cliente_id)
                self.fields['colaborador'].queryset = Colaborador.objects.filter(clinica=cliente.clinica)
            except (ValueError, Cliente.DoesNotExist):
                pass
        elif self.instance.pk:
            self.fields['colaborador'].queryset = Colaborador.objects.filter(clinica=self.instance.cliente.clinica)

    # Validação de data e hora
    def clean(self):
        cleaned_data = super().clean()
        data_e_hora = cleaned_data.get('data_e_hora')

        if data_e_hora:
            if data_e_hora < datetime.now():
                raise forms.ValidationError("A data e hora não podem estar no passado.")
        
        return cleaned_data







