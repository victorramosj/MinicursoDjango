# core/forms.py
from django import forms

class ContatoForm(forms.Form):
    nome = forms.CharField(max_length=100, label="Nome Completo", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Completo'}))
    email = forms.EmailField(max_length=100, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    telefone = forms.CharField(max_length=20, label="Telefone/WhatsApp", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(99) 99999-9999'}))
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mensagem'}))
