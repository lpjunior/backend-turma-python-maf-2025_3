from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from pages.models import Pessoa, MensagemContato


class ContatoForm(forms.ModelForm):
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Digite sua mensagem',
            'class': 'form-control',
            'rows': 4
        }),
        label='Mensagem',
        required=True
    )

    class Meta:
        model = Pessoa
        fields = ['nome', 'email', 'tipo', 'telefone', 'cep', 'cidade', 'estado']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome completo',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Digite seu email',
                'class': 'form-control'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'telefone': forms.TelInput(attrs={
                'placeholder': '(00) 00000-0000',
                'class': 'form-control'
            }),
            'cep': forms.TextInput(attrs={
                'placeholder': '00000-000',
                'class': 'form-control'
            }),
            'cidade': forms.TextInput(attrs={
                'placeholder': 'Digite sua cidade',
                'class': 'form-control'
            }),
            'estado': forms.TextInput(attrs={
                'placeholder': 'Digite seu estado (UF)',
                'class': 'form-control'
            }),
        }

    def clean_nome(self):
        nome = (self.cleaned_data.get('nome') or '').strip()

        if len(nome.split()) < 2:
            raise ValidationError(
                'Informe o nome completo, nome e sobrenome.'
            )

        return nome

    def clean_mensagem(self):
        mensagem = (self.cleaned_data.get('mensagem') or '').strip()

        if len(mensagem.split()) < 5:
            raise ValidationError(
                'A mensagem deve conter pelo menos 5 palavras.'
            )

        return mensagem

    @transaction.atomic
    def save(self, commit=True):
        pessoa, _ = Pessoa.objects.get_or_create(
            email=self.cleaned_data['email'],
            defaults={
                'nome': self.cleaned_data['nome'],
                'telefone': self.cleaned_data.get('telefone'),
                'tipo': self.cleaned_data.get('tipo'),
                'cep': self.cleaned_data.get('cep'),
                'cidade': self.cleaned_data.get('cidade'),
                'estado': self.cleaned_data.get('estado'),
            }
        )

        MensagemContato.objects.create(
            pessoa=pessoa,
            mensagem=self.cleaned_data['mensagem']
        )

        return pessoa


class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = [
            'nome',
            'email',
            'telefone',
            'tipo',
            'cep',
            'cidade',
            'estado',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome completo',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Digite seu email',
                'class': 'form-control'
            }),
            'telefone': forms.TextInput(attrs={
                'placeholder': '(00) 00000-0000',
                'class': 'form-control'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cep': forms.TextInput(attrs={
                'placeholder': '00000-000',
                'class': 'form-control'
            }),
            'cidade': forms.TextInput(attrs={
                'placeholder': 'Digite sua cidade',
                'class': 'form-control'
            }),
            'estado': forms.TextInput(attrs={
                'placeholder': 'UF',
                'class': 'form-control'
            }),
        }

    def clean_cep(self):
        cep = (self.cleaned_data.get('cep') or '').strip()

        if len(cep) != 9 or not cep.replace('-', '').isdigit():
            raise forms.ValidationError(
                'O CEP deve estar no formato 00000-000.'
            )

        return cep

    def clean_nome(self):
        nome = (self.cleaned_data.get('nome') or '').strip()

        if len(nome) < 3:
            raise forms.ValidationError(
                'O nome deve conter pelo menos 3 caracteres.'
            )

        if len(nome.split()) < 2:
            raise forms.ValidationError(
                'Informe o nome completo, nome e sobrenome.'
            )

        return nome

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()

        if not email:
            raise forms.ValidationError('O email é obrigatório.')

        qs = Pessoa.objects.filter(email=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                'Este email já está em uso.'
            )

        return email