from django import forms
from django.core.exceptions import ValidationError

from pages.models import MensagemContato

class ContatoForm(forms.ModelForm):
    class Meta:
        model = MensagemContato
        fields = ['nome', 'email', 'mensagem']

        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome completo',
                'class': 'form-control'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Digite seu email',
                'class': 'form-control'
            }),
            'mensagem': forms.Textarea(attrs={
                'placeholder': 'Digite sua mensagem',
                'class': 'form-control',
                'rows': 4
            })
        }

        labels = {
            'nome': 'Nome',
            'email': 'Email',
            'mensagem': 'Mensagem'
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        palavras = nome.split()

        if len(palavras) < 2:
            raise ValidationError(
                'Informe o nome completo (nome e sobrenome).'
            )

        return nome

    def clean_mensagem(self):
        mensagem = self.cleaned_data.get('mensagem', '').strip()
        quantidade_palavras = len(mensagem.split())

        if quantidade_palavras < 5:
            raise ValidationError(
                'A mensagem deve conter pelo menos 5 palavras.'
            )

        return mensagem