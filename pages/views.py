from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    """
    Essa função é uma 'view'.
    Pense nela como o atendente da sua empresa.
    alguém faz um pedido (request) e ela devolve uma resposta (response).
    """
    hora_atual = datetime.now().hour

    if hora_atual < 12:
        saudacao = "Bom dia!"
    else:
        saudacao = "Boa tarde!"

    contexto = {
        "mensagem": f"{saudacao}! São {datetime.now().strftime("%H:%M")}. Servidor ligado e respondendo. Parabéns, você colocou um back-end no ar.",
        "nome_aluno": "Luis",
        "curso": "Programador Fullstack Python."
    }

    return render(request, 'pages/home.html', contexto)


def contato(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        mensagem = request.POST.get("mensagem")

        contexto = {
            "nome": nome,
            "mensagem": mensagem
        }
        return render(request, 'pages/contato_resultado.html', contexto)

    return render(request, 'pages/contato.html')

def saudacao(request, nome, idade):

    return HttpResponse(
        f"<h1>Olá, {nome} - {idade}! Bem-vindo(a) ao Senac!</h1>"
    )


def sobre(request):
    return render(request, 'pages/sobre.html')


def ajuda(request):
    return render(request, 'pages/ajuda.html')