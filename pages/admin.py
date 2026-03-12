from django.contrib import admin
from .models import Cliente, Solicitacao


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
class MensagemContatoAdmin(admin.ModelAdmin):
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
