import cloudinary.uploader
import logging

from django.db import transaction
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from pages.forms import (
    ClienteForm,
    DepoimentoModeracaoForm,
    DepoimentoRespostaForm,
    OrcamentoForm,
    ProjetoForm,
    SolicitacaoForm,
)
from pages.models import Cliente, Depoimento, Orcamento, Projeto, Solicitacao
from pages.services import enviar_convite_depoimento, enviar_orcamento_email

logger = logging.getLogger(__name__)



def home(request):
    return render(request, 'pages/home.html')

def servicos(request):
    return render(request, 'pages/servicos.html')

def projetos(request):
    projetos_db = Projeto.objects.filter(ativo=True)
    return render(request, 'pages/projetos.html', {'projetos': projetos_db})


@permission_required('pages.view_projeto', raise_exception=True)
def projetos_admin(request):
    projetos_db = Projeto.objects.all()
    return render(request, 'pages/projetos_admin.html', {'projetos': projetos_db})


@permission_required('pages.add_projeto', raise_exception=True)
def projeto_create(request):
    form = ProjetoForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        imagem = request.FILES.get('imagem_file')
        upload = cloudinary.uploader.upload(imagem)

        projeto = form.save(commit=False)
        projeto.imagem = upload.get('secure_url')
        projeto.save()

        return redirect('projetos_admin')

    return render(request, 'pages/projeto_form.html', {'form': form, "acao": "Criar"})


@permission_required('pages.change_projeto', raise_exception=True)
def projeto_update(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)

    if request.method == "POST" and form.is_valid():
        projeto = form.save(commit=False)

        imagem = request.FILES.get('imagem_file')

        if imagem:
            upload = cloudinary.uploader.upload(imagem)
            projeto.imagem = upload.get('secure_url')

        projeto.save()

        return redirect('projetos_admin')

    return render(request, 'pages/projeto_form.html', {'form': form, "acao": "Editar"})


@permission_required('pages.delete_projeto', raise_exception=True)
def projeto_delete(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if request.method == "POST":
        projeto.delete()
        return redirect('projetos_admin')

    return render(request, 'pages/projeto_confirm_delete.html', {'projeto': projeto})


@transaction.atomic
def contato(request):
    if request.method == "POST":
        form = SolicitacaoForm(request.POST)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            tipo = form.cleaned_data['tipo']
            cep = form.cleaned_data['cep']
            cidade = form.cleaned_data['cidade']
            estado = form.cleaned_data['estado']
            mensagem = form.cleaned_data['mensagem']

            cliente, created = Cliente.objects.get_or_create(
                email=email,
                defaults={
                    'nome': nome,
                    'telefone': telefone,
                    'tipo': tipo,
                    'cep': cep,
                    'cidade': cidade,
                    'estado': estado,
                    'ativo': True
                }
            )

            if not created:
                cliente.nome = nome
                cliente.telefone = telefone
                cliente.tipo = tipo
                cliente.cep = cep
                cliente.cidade = cidade
                cliente.estado = estado
                cliente.ativo = True
                cliente.save()

            Solicitacao.objects.create(
                cliente=cliente,
                mensagem=mensagem,
                status='pendente'
            )

            return render(
                request,
                'pages/contato_sucesso.html',
                {
                    'nome': nome,
                    'email': email
                }
            )

    else:
        form = SolicitacaoForm()

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
    except Exception:
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
@permission_required('pages.view_cliente', raise_exception=True)
def clientes(request):
    clientes_qs = (
        Cliente.objects
        .annotate(total_solicitacoes=Count('solicitacoes'))
        .order_by('nome')
    )

    return render(request, 'pages/clientes.html', { 'clientes': clientes_qs })

@permission_required('pages.view_cliente', raise_exception=True)
def cliente_detalhe(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    solicitacoes = cliente.solicitacoes.all().order_by('-data_envio')

    return render(
        request,
        'pages/cliente_detalhe.html',
        {
            'cliente': cliente,
            'solicitacoes': solicitacoes
        }
    )

@permission_required('pages.add_cliente', raise_exception=True)
def cliente_create(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()

    return render(request, 'pages/cliente_form.html', {'form': form, "acao": "Criar"})

@permission_required('pages.change_cliente', raise_exception=True)
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

@permission_required('pages.delete_cliente', raise_exception=True)
def cliente_delete(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        cliente.delete()
        return redirect('clientes')

    return render(request, 'pages/cliente_confirm_delete.html', {'cliente': cliente})


# ========================
#    Gestão, Solicitações
# ========================
@permission_required('pages.view_solicitacao', raise_exception=True)
def lista_solicitacoes(request):
    solicitacoes_qs = (
        Solicitacao.objects
        .select_related('cliente')
        .order_by('-data_envio')
    )
    return render(request, 'pages/lista_solicitacoes.html', {'solicitacoes': solicitacoes_qs})

@permission_required('pages.view_solicitacao', raise_exception=True)
def detalhe_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(Solicitacao, id=solicitacao_id)

    if solicitacao.status == 'pendente':
        solicitacao.status = 'lido'
        solicitacao.save(update_fields=['status'])

    orcamento = getattr(solicitacao, 'orcamento', None)

    return render(
        request, 'pages/solicitacao_detalhe.html', {
            'solicitacao': solicitacao,
            'orcamento': orcamento
        }
    )

@permission_required('pages.add_orcamento', raise_exception=True)
@transaction.atomic
def criar_orcamento(request, solicitacao_id):
    solicitacao = get_object_or_404(Solicitacao, id=solicitacao_id)

    if Orcamento.objects.filter(solicitacao=solicitacao).exists():
        messages.warning(request, 'Esta solicitação já possui um orçamento associado.')
        return redirect('detalhe_solicitacao', solicitacao_id)

    if request.method == "POST":
        form = OrcamentoForm(request.POST)

        if form.is_valid():
            orcamento = form.save(commit=False)
            orcamento.solicitacao = solicitacao
            orcamento.save()

            solicitacao.status = 'respondido'
            solicitacao.save(update_fields=['status'])

            enviar_orcamento_email(solicitacao, orcamento)

            messages.success(request, 'Orçamento criado e enviado por email.')
            return redirect('detalhe_solicitacao', solicitacao_id)
    else:
        form = OrcamentoForm()

    return render(request, 'pages/orcamento_form.html', {
        'form': form,
        'solicitacao': solicitacao
    })

def depoimentos(request):
    depoimentos_qs = cache.get_or_set(
        "pagina_depoimentos_aprovados",
        lambda: list(
            Depoimento.objects.filter(status="aprovado", ativo=True)
            .select_related("cliente")
            .order_by("-respondido_em", "-criado_em")[:12]
        ),
        300,
    )

    depoimentos_iniciais = depoimentos_qs[:6]
    depoimentos_extras = depoimentos_qs[6:12]

    return render(
        request,
        "pages/depoimentos.html",
        {
            "depoimentos_iniciais": depoimentos_iniciais,
            "depoimentos_extras": depoimentos_extras,
            "tem_mais_depoimentos": len(depoimentos_qs) > 6,
        },
    )


def feedback_publico(request, token):
    depoimento = get_object_or_404(Depoimento, token=token, ativo=True)

    if depoimento.respondido_em:
        return render(
            request,
            "pages/feedback_sucesso.html",
            {"depoimento_ja_respondido": True},
        )

    form = DepoimentoRespostaForm(request.POST or None, instance=depoimento)

    if request.method == "POST" and form.is_valid():
        depoimento = form.save(commit=False)
        depoimento.status = "pendente"
        depoimento.respondido_em = timezone.now()
        depoimento.save()

        cache.delete("home_depoimentos_aprovados")
        cache.delete("pagina_depoimentos_aprovados")

        return render(
            request,
            "pages/feedback_sucesso.html",
            {"depoimento_ja_respondido": False},
        )

    return render(
        request,
        "pages/feedback_form.html",
        {"form": form, "depoimento": depoimento},
    )


@login_required
@permission_required("pages.view_depoimento", raise_exception=True)
def depoimentos_admin(request):
    status = request.GET.get("status", "")
    depoimentos_qs = Depoimento.objects.select_related("cliente", "solicitacao").all()

    if status:
        depoimentos_qs = depoimentos_qs.filter(status=status)

    return render(
        request,
        "pages/depoimentos_admin.html",
        {
            "depoimentos": depoimentos_qs,
            "status_filtro": status,
        },
    )


@login_required
@permission_required("pages.change_depoimento", raise_exception=True)
def depoimento_moderar(request, depoimento_id):
    depoimento = get_object_or_404(
        Depoimento.objects.select_related("cliente", "solicitacao"),
        id=depoimento_id,
    )
    form = DepoimentoModeracaoForm(request.POST or None, instance=depoimento)

    if request.method == "POST" and form.is_valid():
        depoimento = form.save(commit=False)
        depoimento.moderado_em = timezone.now()
        depoimento.save()

        cache.delete("home_depoimentos_aprovados")
        cache.delete("pagina_depoimentos_aprovados")

        messages.success(request, "Depoimento atualizado com sucesso.")
        return redirect("depoimentos_admin")

    return render(
        request,
        "pages/depoimento_moderar.html",
        {
            "depoimento": depoimento,
            "form": form,
        },
    )


@login_required
@permission_required("pages.add_depoimento", raise_exception=True)
def solicitar_depoimento(request, solicitacao_id):
    solicitacao = get_object_or_404(
        Solicitacao.objects.select_related("cliente"),
        id=solicitacao_id,
    )

    depoimento, created = Depoimento.objects.get_or_create(
        solicitacao=solicitacao,
        defaults={
            "cliente": solicitacao.cliente,
            "status": "pendente",
        },
    )

    if depoimento.respondido_em:
        messages.warning(
            request,
            "Já existe um depoimento respondido para esta solicitação.",
        )
        return redirect("solicitacao_detalhe", solicitacao_id=solicitacao.id)

    depoimento.solicitado_em = timezone.now()
    depoimento.save(update_fields=["solicitado_em"])

    enviar_convite_depoimento(request, depoimento)

    messages.success(
        request,
        "Convite de depoimento enviado com sucesso.",
    )

    return redirect("solicitacao_detalhe", solicitacao_id=solicitacao.id)