from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.http import HttpResponse
from django.shortcuts import render

from pages.forms import ContatoForm


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
        form = ContatoForm(request.POST) # Cria um formulário com os dados do POST

        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            mensagem = form.cleaned_data['mensagem']

            # persistir os dados na base..

            return render(request, 'pages/contato_resultado.html', {
                "nome": nome
            })
    else:
        form = ContatoForm() # Cria um formulário vazio

    return render(request, 'pages/contato.html', { 'form': form })

def saudacao(request, nome, idade):

    return HttpResponse(
        f"<h1>Olá, {nome} - {idade}! Bem-vindo(a) ao Senac!</h1>"
    )


def sobre(request):
    return render(request, 'pages/sobre.html')


def ajuda(request):
    return render(request, 'pages/ajuda.html')