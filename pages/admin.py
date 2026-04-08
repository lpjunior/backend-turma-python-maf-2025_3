from django.contrib import admin
from .models import Cliente, Solicitacao, Orcamento, Projeto, Depoimento


@admin.register(Cliente) # Registrar o modelo Pessoa no admin. É equivalente a admin.site.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'total_mensagens')
    search_fields = ('nome', 'email')
    ordering = ('nome',)
    list_per_page = 20

    def total_mensagens(self, obj):
        return obj.mensagens.count()

    total_mensagens.short_description = 'Total de Mensagens'


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'email',
        'data_envio',
        'mensagem_resumida',
    )

    search_fields = (
        'cliente__nome',
        'cliente__email',
        'mensagem',
    )

    list_filter = (
        'data_envio',
        'cliente',
    )

    ordering = ('-data_envio',)
    date_hierarchy = 'data_envio'
    list_select_related = ('cliente',)
    list_per_page = 20
    readonly_fields = ('data_envio',)

    def email(self, obj):
        return obj.cliente.email

    email.short_description = 'Email'

    def mensagem_resumida(self, obj):
        return obj.mensagem[:50] + '...' if len(obj.mensagem) > 50 else obj.mensagem

    mensagem_resumida.short_description = 'Mensagem'


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "solicitacao", "valor", "status", "criado_em")
    search_fields = ("titulo", "solicitacao__cliente__nome")
    list_filter = ("status", "criado_em")


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "ativo", "criado_em")
    search_fields = ("titulo", "categoria", "descricao")
    list_filter = ("categoria", "ativo")


@admin.register(Depoimento)
class DepoimentoAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "solicitacao",
        "nota",
        "nps",
        "status",
        "respondido_em",
        "moderado_em",
    )
    search_fields = ("cliente__nome", "cliente__email", "comentario")
    list_filter = ("status", "nota", "anonimizar_nome")