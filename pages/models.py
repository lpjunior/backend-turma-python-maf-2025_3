from django.db import models


class Cliente(models.Model):
    TIPO_CHOICES = [
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    ]

    nome = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(max_length=150, blank=False, null=False)

    telefone = models.CharField(max_length=20, blank=False, null=False)

    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='pf')

    cep = models.CharField(max_length=9, blank=False, null=False)
    cidade = models.CharField(max_length=100, blank=False, null=False, default='')
    estado = models.CharField(max_length=2, blank=False, null=False, default='')

    data_cadastro = models.DateTimeField(auto_now_add=True)

    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = 'pessoas'

    def __str__(self):
        return f'{self.nome} <{self.email}> - status: {self.ativo}'

class Solicitacao(models.Model):

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('lido', 'Lido'),
        ('respondido', 'Respondido')
    ]

    pessoa = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='mensagens'
    )

    mensagem = models.TextField(blank=False, null=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mensagens'
        ordering = ['-data_envio']

    def __str__(self):
        return f'Solicitação de: {self.pessoa.nome} <{self.pessoa.email}>'