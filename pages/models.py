import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Cliente(models.Model):
    TIPO_CHOICES = [
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    ]

    nome = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(max_length=150, blank=False, null=False, unique=True)
    telefone = models.CharField(max_length=20, blank=False, null=False)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='pf')
    cep = models.CharField(max_length=9, blank=False, null=False)
    cidade = models.CharField(max_length=100, blank=False, null=False, default='')
    estado = models.CharField(max_length=2, blank=False, null=False, default='')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = 'clientes'
        ordering = ['-data_cadastro']

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

class Projeto(models.Model):
    CATEGORIA_CHOICES = [
        ('residencial',  'Residencial'),
        ('comercial', 'Comercial'),
        ('rural', 'Rural'),
        ('governamental', 'Governamental'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=False, null=False)
    tagline = models.CharField(max_length=255)
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='residencial'
    )
    imagem = models.URLField()
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = 'projetos'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.titulo} - {self.get_categoria_display()}'

class Depoimento(models.Model):
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("aprovado", "Aprovado"),
        ("rejeitado", "Rejeitado"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="depoimentos",
    )
    solicitacao = models.ForeignKey(
        Solicitacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="depoimentos",
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
    )
    nps = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )
    comentario = models.TextField(blank=True, default="")
    anonimizar_nome = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendente",
    )
    solicitado_em = models.DateTimeField(null=True, blank=True)
    respondido_em = models.DateTimeField(null=True, blank=True)
    moderado_em = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "depoimentos"
        ordering = ["-respondido_em", "-criado_em"]

    def __str__(self):
        return f"Depoimento de {self.cliente.nome} - {self.get_status_display()}"

    @property
    def nome_exibicao(self):
        if not self.anonimizar_nome:
            return self.cliente.nome

        partes = self.cliente.nome.split()
        if not partes:
            return "Cliente"

        if len(partes) == 1:
            return f"{partes[0][0]}***"

        return f"{partes[0]} {partes[1][0]}***"