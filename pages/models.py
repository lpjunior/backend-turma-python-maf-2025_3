from django.db import models


class Pessoa(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=150, blank=False, null=False)

    class Meta:
        db_table = 'pessoas'

    def __str__(self):
        return self.nome

class MensagemContato(models.Model):
    pessoa = models.ForeignKey(
        Pessoa,  # modelo relacionado
        on_delete=models.CASCADE,  # se a pessoa for deletada, as mensagens relacionadas a ela também serão deletadas
        related_name='mensagens' # nome do atributo que será criado na classe Pessoa para acessar as mensagens relacionadas a ela (ex: pessoa.mensagens.all() para obter todas as mensagens de uma pessoa)
    )
    mensagem = models.TextField(blank=False, null=False)
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mensagens'
        ordering = ['-data_envio']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.pessoa.email}'