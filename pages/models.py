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
        db_table = 'clientes'

    def __str__(self):
        return f'{self.nome} <{self.email}> - status: {self.ativo}'

class Solicitacao(models.Model):

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('lido', 'Lido'),
        ('respondido', 'Respondido')
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='solicitacoes'
    )

    mensagem = models.TextField(blank=False, null=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'solicitacoes'
        ordering = ['-data_envio']

    def __str__(self):
        return f'Solicitação de: {self.cliente.nome} <{self.cliente.email}>'

class Orcamento(models.Model):

    STATUS_CHOICES = [
        ('em_analise', 'Em Análise'),
        ('enviado', 'Enviado'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado')
    ]

    solicitacao = models.OneToOneField(
        Solicitacao,
        on_delete=models.CASCADE,
        related_name='orcamento'
    )

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=False, null=False)

    valor = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='em_analise'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orcamentos'
        ordering = ['-modificado_em']

    def __str__(self):
        return f'Orçamento de: {self.id}, {self.solicitacao.cliente.nome} <{self.solicitacao.cliente.email}>'