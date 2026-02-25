from django.contrib import admin
from .models import Pessoa, MensagemContato

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'total_mensagens')
    search_fields = ('nome', 'email')
    ordering = ('nome',)
    list_per_page = 20

    def total_mensagens(self, obj):
        return obj.mensagens.count()

    total_mensagens.short_description = 'Total de Mensagens'


@admin.register(MensagemContato)
class MensagemContatoAdmin(admin.ModelAdmin):
    list_display = (
        'pessoa',
        'email',
        'data_envio',
        'mensagem_resumida',
    )

    search_fields = (
        'pessoa__nome',
        'pessoa__email',
        'mensagem',
    )

    list_filter = (
        'data_envio',
        'pessoa',
    )

    ordering = ('-data_envio',)
    date_hierarchy = 'data_envio'
    list_select_related = ('pessoa',)
    list_per_page = 20
    readonly_fields = ('data_envio',)

    def email(self, obj):
        return obj.pessoa.email

    email.short_description = 'Email'

    def mensagem_resumida(self, obj):
        return obj.mensagem[:50] + '...' if len(obj.mensagem) > 50 else obj.mensagem

    mensagem_resumida.short_description = 'Mensagem'