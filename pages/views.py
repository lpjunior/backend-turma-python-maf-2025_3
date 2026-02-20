from django.contrib.auth import authenticate, login, logout # funções para autenticação de usuários
from django.contrib.auth.decorators import login_required # decorator para restringir o acesso a uma view apenas para usuários autenticados

from datetime import datetime # módulo para trabalhar com datas e horas

from django.db.models import Count # função para realizar contagem de objetos relacionados em uma consulta ao banco de dados (ex: contar quantas mensagens cada pessoa tem)
from django.http import HttpResponse # classe para criar respostas HTTP personalizadas
from django.shortcuts import render, redirect # funções para renderizar templates e redirecionar para outras URLs

from pages.forms import ContatoForm # formulário para contato, definido em pages/forms.py
from pages.models import MensagemContato, Pessoa # modelos para mensagens de contato e pessoas, definidos em pages/models.py


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

@login_required
def mensagens(request):
    mensagens = MensagemContato.objects.all()
    contexto = { 'mensagens': mensagens }
    return render(request, 'pages/mensagens.html', contexto)

@login_required
def pessoas(request):
    """
    Essa view é para exibir a lista de pessoas cadastradas no banco de dados.
    """
    # QuerySet é uma coleção de objetos do banco de dados. Ele é criado a partir do modelo (model) e pode ser filtrado, ordenado, etc.
    lista = ( # consulta para obter a lista de pessoas com a contagem de mensagens relacionadas a cada pessoa
        Pessoa.objects
        .annotate(total_mensagens=Count('mensagens')) # adiciona um campo total_mensagens com a contagem de mensagens relacionadas a cada pessoa
        .order_by("nome") # ordena por nome
    )

    contexto = { 'pessoas': lista }
    return render(request, 'pages/pessoas.html', contexto)

def login_view(request):
    if request.method == "POST":
        username = (request.POST.get('username') or '').strip() # obtém o nome de usuário do formulário, garantindo que seja uma string e removendo espaços em branco
        password = (request.POST.get('password') or '').strip() # obtém a senha do formulário, garantindo que seja uma string e removendo espaços em branco

        # Autentica o usuário usando as credenciais fornecidas. Se as credenciais forem válidas, retorna um objeto User; caso contrário, retorna None.
        user = authenticate(request, username=username, password=password)
        # authenticate verifica se as credenciais do usuário são válidas. Ele consulta o banco de dados para encontrar um usuário com o nome de usuário fornecido e verifica se a senha corresponde à senha armazenada para esse usuário. Se as credenciais forem válidas, ele retorna um objeto User; caso contrário, retorna None.

        if user is not None:
            login(request, user) # login inicia a sessão do usuário autenticado, associando o usuário ao request. Isso permite que o Django reconheça o usuário em requisições subsequentes e forneça acesso a áreas restritas do site.
            return redirect('area_restrita')
        else:
            return render(request, 'pages/login.html', {'error': 'Credenciais inválidas'})

    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request) # logout encerra a sessão do usuário, removendo as informações de autenticação associadas ao request. Isso efetivamente desloga o usuário do site, impedindo o acesso a áreas restritas até que ele faça login novamente.
    return redirect('login')

@login_required # decorator que restringe o acesso a essa view apenas para usuários autenticados. Se um usuário não autenticado tentar acessar essa view, ele será redirecionado para a página de login.
def area_restrita(request):
    # A view de área restrita é decorada com @login_required, o que significa que apenas usuários autenticados podem acessá-la. Se um usuário não autenticado tentar acessar essa view, ele será redirecionado para a página de login.
    return render(request, 'pages/restrita.html')