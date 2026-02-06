from datetime import datetime
from email import message

from django.http import HttpResponse
from django.shortcuts import render

from pages.forms import ContatoForm
from pages.models import MensagemContato


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
    # Se o usuário apenas acessou a página (GET),
    # criamos um formulário vazio para exibição
    if request.method == "GET":
        form = ContatoForm()

    # Se o usuário enviou o formulário (POST),
    # criamos o formulário com os dados enviados
    else:
        form = ContatoForm(request.POST)

        # is_valid executa TODAS as validações do formulário
        if form.is_valid():
            # cleaned_data contém apenas dados já validados
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']

            # Salva os dados no banco de dados
            form.save()

            # Exibe uma mensagem de sucesso
            return render(
                request,
                'pages/contato_resultado.html',
                {
                    'nome': nome,
                    'email': email
                }
            )

    # Se for GET ou se houver erro no POST,
    # o formulário é reexibido
    return render(
        request,
        'pages/contato.html',
        {'form': form}
    )

def saudacao(request, nome, idade):

    return HttpResponse(
        f"<h1>Olá, {nome} - {idade}! Bem-vindo(a) ao Senac!</h1>"
    )


def sobre(request):
    return render(request, 'pages/sobre.html')


def ajuda(request):
    return render(request, 'pages/ajuda.html')

def mensagens(request):
    mensagens = MensagemContato.objects.all()
    contexto = { 'mensagens': mensagens }
    return render(request, 'pages/mensagens.html', contexto)