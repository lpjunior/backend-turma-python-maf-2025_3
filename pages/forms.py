from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from pages.models import Cliente, Solicitacao, Orcamento, Projeto, Depoimento


class SolicitacaoForm(forms.ModelForm):
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Descreva sua necessidade',
            'class': 'form-control',
            'rows': 4
        }),
        label='Descrição',
        required=True
    )

    class Meta:
        model = Cliente
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
                'A descrição deve conter pelo menos 5 palavras.'
            )

        return mensagem

    @transaction.atomic
    def save(self, commit=True):
        cliente, _ = Cliente.objects.get_or_create(
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

        Solicitacao.objects.create(
            cliente=cliente,
            solicitacao=self.cleaned_data['descricao']
        )

        return cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
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
                'class': 'form-select'
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

    def clean_telefone(self):
        telefone = (self.cleaned_data.get('telefone') or '').strip()

        if len(telefone) < 10 or not telefone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError(
                'O telefone deve conter pelo menos 10 dígitos e estar no formato (00) 00000-0000.'
            )

        return telefone

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

        qs = Cliente.objects.filter(email=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                'Este email já está em uso.'
            )

        return email

class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ['titulo', 'descricao', 'valor', 'status']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            })
        }

class ProjetoForm(forms.ModelForm):
    imagem_file = forms.ImageField(required=False)

    class Meta:
        model = Projeto
        fields = ['titulo', 'descricao', 'tagline', 'categoria', 'ativo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Controle do campo imagem (já existente)
        if not self.instance or not self.instance.imagem:
            self.fields['imagem_file'].required = True
        else:
            self.fields['imagem_file'].required = False

        # Remove o campo ativo no CREATE
        if not self.instance or not self.instance.pk:
            self.fields.pop('ativo')
        else:
            self.fields['ativo'].widget.attrs.update({
                'class': 'form-check-input'
            })

    def clean_titulo(self):
        titulo = (self.cleaned_data.get('titulo') or '').strip()

        if len(titulo) < 3:
            raise forms.ValidationError('O titulo deve conter pelo menos 3 caracteres.')

        return titulo

    def clean_descricao(self):
        descricao = (self.cleaned_data.get('descricao') or '').strip()

        if len(descricao) < 10:
            raise forms.ValidationError('A descrição deve conter pelo menos 10 caracteres.')

        return descricao

    def clean_tagline(self):
        tagline = (self.cleaned_data.get('tagline') or '').strip()

        if len(tagline) < 10:
            raise forms.ValidationError('A tagline deve conter pelo menos 10 caracteres.')

        return tagline

    def clean_imagem_file(self):
        imagem = self.cleaned_data.get('imagem_file')

        if not imagem and not self.instance.imagem:
            raise forms.ValidationError('A imagem é obrigatória.')

        return imagem

class DepoimentoRespostaForm(forms.ModelForm):
    class Meta:
        model = Depoimento
        fields = ["nota", "nps", "comentario", "anonimizar_nome"]
        widgets = {
            "nota": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 5,
                }
            ),
            "nps": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 10,
                }
            ),
            "comentario": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Conte como foi sua experiência com a SolarTech",
                }
            ),
            "anonimizar_nome": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_comentario(self):
        comentario = (self.cleaned_data.get("comentario") or "").strip()

        if len(comentario.split()) < 5:
            raise ValidationError("O comentário deve conter pelo menos 5 palavras.")

        return comentario


class DepoimentoModeracaoForm(forms.ModelForm):
    class Meta:
        model = Depoimento
        fields = ["status"]
        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }