from django import forms # importando o módulo de formulários do Django

# serve para validação.
from django.core.exceptions import ValidationError

class ContatoForm(forms.Form): # ContatoForm especializa forms.Form
    nome = forms.CharField( # forms.CharField define por padrão um campo de texto <input type="text">
        label='Nome',
        min_length=3, # substitui o if len(nome) < 3
        required=True, # substitui o if not nome
        widget=forms.TextInput(attrs= {
            'placeholder': 'Digite seu nome',
            'class': 'form-control'
        })
    )

    email = forms.EmailField( # forms.EmailField valida o email automaticamente incluindo coisas além de só @
        label='Email',
        required=True, # substitui o if not email
        widget = forms.TextInput(attrs={
        'placeholder': 'Digite seu email',
        'class': 'form-control'
    })
    )

    mensagem = forms.CharField(
        label='Mensagem',
        # mudar o tipo do campo para <textarea>
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Digite sua mensagem',
                'class': 'form-control',
                'rows': 4
        }),
        min_length=10 # substitui o if len(mensagem) < 10
    )

    # método especial do Django Forms. Tudo que estiver em clean_<nome_do_campo>
    #  roda na validação e server para regras extras daquele campo
    def clean_mensagem(self):
        mensagem = self.cleaned_data.get('mensagem', "").strip()
        quantidade_palavras = len(mensagem.split())

        if quantidade_palavras < 5:
            raise ValidationError("A mensagem deve conter pelo menos 5 palavras.")

        return mensagem