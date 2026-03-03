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
        fields = ['nome', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome completo',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Digite seu email',
                'class': 'form-control'
            })
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome.split()) < 2:
            raise ValidationError(
                'Informe o nome completo, nome e sobrenome.'
            )
        return nome

    def clean_mensagem(self):
        mensagem = self.cleaned_data.get('mensagem', '').strip()
        if len(mensagem.split()) < 5:
            raise ValidationError(
                'A mensagem deve conter pelo menos 5 palavras.'
            )
        return mensagem

    @transaction.atomic # decorator para garantir que as operações dentro do método sejam atômicas, ou seja, ou todas são executadas com sucesso ou nenhuma é aplicada ao banco de dados em caso de erro
    def save(self, commit=True):
        # salva ou recupera a Pessoa
        pessoa, _ = Pessoa.objects.get_or_create(
            email=self.cleaned_data['email'], # chave utilizada para buscar a Pessoa
            defaults={'nome': self.cleaned_data['nome']} # caso a Pessoa não exista, cria uma nova com esse nome
        )

        # cria a MensagemContato vinculada
        MensagemContato.objects.create(
            pessoa=pessoa,
            mensagem=self.cleaned_data['mensagem']
        )

        return pessoa

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome completo',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Digite seu email',
                'class': 'form-control'
            })
        }

    def clean_nome(self):
        nome = (self.cleaned_data.get('nome', '') or '').strip()

        if len(nome) < 3:
            raise forms.ValidationError('O nome deve conter pelo menos 3 caracteres.')

        if len(nome.split()) < 2:
            raise forms.ValidationError('Informe o nome completo, nome e sobrenome.')

        return nome

    def clean_email(self):
        email = (self.cleaned_data.get('email', '') or '').strip().lower()

        if not email:
            raise forms.ValidationError('O email é obrigatório.')

        qs = Pessoa.objects.filter(email=email)

        # Se for edição, excluir o próprio registro da verificação
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('Este email já está em uso.')

        return email