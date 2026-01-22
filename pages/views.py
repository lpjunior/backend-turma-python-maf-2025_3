from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    """
    Essa função é uma 'view'.
    Pense nela como o atendente da sua empresa.
    alguém faz um pedido (request) e ela devolve uma resposta (response).
    """

    contexto = {
        "mensagem": "Servidor ligado e respondendo. Parabéns, você colocou um back-end no ar.",
        "nome_aluno": "Luis",
        "curso": "Programador Fullstack Python."
    }

    return render(request, 'pages/home.html', contexto)


def contato(request):

    return render(request, 'pages/contato.html')


def saudacao(request, nome, idade):
    return HttpResponse(
        f"<h1>Olá, {nome} - {idade}! Bem-vindo(a) ao Senac!</h1>"
    )