import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, \
    get_object_or_404

from pages.forms import SolicitacaoForm, ClienteForm, OrcamentoForm
from pages.models import Solicitacao, Cliente

logger = logging.getLogger(__name__)

# ========================
#    Páginas Públicas
# ========================
def home(request):
    return render(request, 'pages/home.html')

def servicos(request):
    return render(request, 'pages/servicos.html')

def projetos(request):
    return render(request, 'pages/projetos.html')

def depoimentos(request):
    return render(request, 'pages/depoimentos.html')

def contato(request):
    if request.method == "GET":
        form = SolicitacaoForm()

    else:
        form = SolicitacaoForm(request.POST)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']

            # Salva os dados no banco de dados
            form.save()

            # Exibe uma mensagem de sucesso
            return render(
                request,
                'pages/contato_sucesso.html',
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


# ========================
#    Autenticação
# ========================
def login_view(request):
    if request.method == "POST":
        username = (request.POST.get('username') or '').strip()
        password = (request.POST.get('password') or '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'pages/login.html', {'error': 'Credenciais inválidas'})

    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ========================
#    Tratamento de Erros
# ========================
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

# ========================
#    Gestão, Dashboard
# ========================
@login_required
def dashboard(request):
    total_solicitacoes = Solicitacao.objects.count()

    pendentes = Solicitacao.objects.filter(status='pendente').count()
    lidas = Solicitacao.objects.filter(status='lido').count()
    respondidas = Solicitacao.objects.filter(status='respondido').count()

    total_clientes = Cliente.objects.count()

    contexto = {
        'total_solicitacoes': total_solicitacoes,
        'pendentes': pendentes,
        'lidas': lidas,
        'respondidas': respondidas,
        'total_clientes': total_clientes
    }

    return render(request, 'pages/dashboard.html', contexto)

# ========================
#    Gestão, Clientes
# ========================
@permission_required(
    'pages.view_cliente',
    raise_exception=True
)
def clientes(request):
    clientes_qs = (
        Cliente.objects
        .annotate(total_solicitacoes=Count('mensagens'))
        .order_by('nome')
    )

    return render(request, 'pages/clientes.html', { 'clientes': clientes_qs })

@permission_required(
    'pages.view_cliente',
    raise_exception=True
)

def cliente_detalhe(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)

    solicitacoes = cliente.mensagens.all().order_by('-data_envio')

    return render(
        request,
        'pages/cliente_detalhe.html',
        {
            'cliente': cliente,
            'solicitacoes': solicitacoes
        }
    )

@permission_required(
    'pages.add_cliente',
    raise_exception=True
)
def cliente_create(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()

    return render(request, 'pages/cliente_form.html', {'form': form, "acao": "Criar"})

@permission_required(
    'pages.change_cliente',
    raise_exception=True
)
def cliente_update(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'pages/cliente_form.html', {'form': form, "acao": "Editar"})

@permission_required(
    'pages.delete_cliente',
    raise_exception=True
)
def cliente_delete(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        cliente.delete()
        return redirect('clientes')

    return render(request, 'pages/cliente_confirm_delete.html', {'cliente': cliente})


# ========================
#    Gestão, Solicitações
# ========================
@permission_required(
    'pages.view_solicitacao',
    raise_exception=True
)
def lista_solicitacoes(request):
    solicitacoes_qs = (
        Solicitacao.objects
        .select_related('cliente')
        .all()
    )
    return render(request, 'pages/lista_solicitacoes.html', {'solicitacoes': solicitacoes_qs})

@permission_required(
    'pages.view_solicitacao',
    raise_exception=True
)
def detalhe_solicitacao(request, id):
    solicitacao = get_object_or_404(Solicitacao, id=id)
    orcamento = getattr(solicitacao, 'orcamento', None)

    return render(
        request, 'pages/solicitacao_detalhe.html', {
            'solicitacao': solicitacao,
            'orcamento': orcamento
        }
    )

@permission_required(
    'pages.add_orcamento',
    raise_exception=True
)
def criar_orcamento(request, solicitacao_id):
    solicitacao = get_object_or_404(Solicitacao, id=solicitacao_id)

    if hasattr(solicitacao, 'orcamento'):
        return redirect('detalhe_solicitacao', solicitacao_id)

    form = OrcamentoForm(request.POST or None)

    if form.is_valid():
        orcamento = form.save(commit=False)
        orcamento.solicitacao = solicitacao
        orcamento.save()

        return redirect('detalhe_solicitacao', solicitacao_id)

    return render(request, 'pages/orcamento_form.html', {
        'form': form,
        'solicitacao': solicitacao
    })


