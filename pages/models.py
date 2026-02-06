from django.db import models

# models.Model - indica que essa classe representa uma tabela no banco de dados
# CharField - usado para campos de texto curtos.
# TextField - usado para campos de texto longos.
# EmailField - usado para campos de e-mail.
# DateTimeField - usado para campos de data e hora.

class MensagemContato(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=150, blank=False, null=False)
    mensagem = models.TextField(blank=False, null=False)
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta: # configurações adicionais para a classe
        db_table = 'mensagens' # nome da tabela no banco de dados
        ordering = ['-data_envio']

    def __str__(self):
        return f'{self.nome} - {self.email}'