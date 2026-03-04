import logging
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, \
    get_object_or_404

from pages.forms import ContatoForm, PessoaForm
from pages.models import MensagemContato, Pessoa

logger = logging.getLogger(__name__)

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
    if request.method == "GET":
        form = ContatoForm()

    else:
        form = ContatoForm(request.POST)

        if form.is_valid():
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

    return render(
        request,
        'pages/contato.html',
        {'form': form}
    )

def sobre(request):
    return render(request, 'pages/sobre.html')

def ajuda(request):
    return render(request, 'pages/ajuda.html')

@permission_required(
    'pages.view_mensagemcontato',
    raise_exception=True
)
def mensagens(request):
    mensagens = MensagemContato.objects.all()
    contexto = { 'mensagens': mensagens }
    return render(request, 'pages/mensagens.html', contexto)

@permission_required(
    'pages.view_pessoa',
    raise_exception=True
)
def pessoas(request):
    """
    Essa view é para exibir a lista de pessoas cadastradas no banco de dados.
    """
    lista = (
        Pessoa.objects
        .annotate(total_mensagens=Count('mensagens'))
        .order_by("nome") # ordena por nome
    )

    contexto = { 'pessoas': lista }
    return render(request, 'pages/pessoas.html', contexto)

def login_view(request):
    if request.method == "POST":
        username = (request.POST.get('username') or '').strip()
        password = (request.POST.get('password') or '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('area_restrita')
        else:
            return render(request, 'pages/login.html', {'error': 'Credenciais inválidas'})

    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def area_restrita(request):
    return render(request, 'pages/restrita.html')

def erro_403(request, exception=None):
    try:
        if exception:
            logger.warning(
                "Erro 403 | Usuário: %s | Path: %s | Detalhes: %s",
                request.user.username if request.user.is_authenticated else 'Anônimo',
                request.path,
                str(exception)
            )

        return render(request, 'pages/403.html', status=403)
    except Exception as e:
        logger.warning(
            "Falha ao renderizar página 403 | Usuário: %s | Path: %s | Detalhes do erro: %s",
            request.user.username if request.user.is_authenticated else 'Anônimo',
            request.path,
            str(exception)
        )

        return HttpResponseForbidden("Acesso negado. Você não tem permissão para acessar esta página.")

@permission_required(
    'pages.add_pessoa',
    raise_exception=True
)
def pessoa_create(request):
    if request.method == "POST":
        form = PessoaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('pessoas')
    else:
        form = PessoaForm()

    return render(request, 'pages/pessoa_form.html', {'form': form, "acao": "Criar"})

@permission_required(
    'pages.change_pessoa',
    raise_exception=True
)
def pessoa_update(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)

    if request.method == "POST":
        form = PessoaForm(request.POST, instance=pessoa)

        if form.is_valid():
            form.save()
            return redirect('pessoas')
    else:
        form = PessoaForm(instance=pessoa)

    return render(request, 'pages/pessoa_form.html', {'form': form, "acao": "Editar"})

@permission_required(
    'pages.delete_pessoa',
    raise_exception=True
)
def pessoa_delete(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)

    if request.method == "POST":
        pessoa.delete()
        return redirect('pessoas')

    return render(request, 'pages/pessoa_confirm_delete.html', {'pessoa': pessoa})

@login_required
def dashboard(request):
    total_solicitacoes = MensagemContato.objects.count()

    pendentes = MensagemContato.objects.filter(status='pendente').count()
    lidas = MensagemContato.objects.filter(status='lido').count()
    respondidas = MensagemContato.objects.filter(status='respondido').count()

    total_clientes = Pessoa.objects.count()

    contexto = {
        'total_solicitacoes': total_solicitacoes,
        'pendentes': pendentes,
        'lidas': lidas,
        'respondidas': respondidas,
        'total_clientes': total_clientes
    }

    return render(request, 'pages/dashboard.html', contexto)