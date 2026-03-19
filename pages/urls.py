from . import views
from django.urls import path

urlpatterns = [
    # ========================
    #      Area publica
    # ========================
    path('', views.home, name='home'),
    path('servicos/', views.servicos, name='servicos'),
    path('projetos/', views.projetos, name='projetos'),
    path('depoimentos/', views.depoimentos, name='depoimentos'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ========================
    #   Area administrativa
    # ========================
    path('gestao/', views.dashboard, name='dashboard'),
    path('gestao/clientes', views.clientes, name='clientes'),
    path('gestao/cliente/novo/', views.cliente_create, name='cliente_create'),
    path('gestao/cliente/<int:id_cliente>', views.cliente_detalhe, name='cliente_detalhe'),
    path('gestao/cliente/editar/', views.cliente_update, name='cliente_update'),
    path('gestao/cliente/excluir/', views.cliente_delete, name='cliente_delete'),


    path('contato/', views.contato, name='contato'),

    path('solicitacoes/', views.lista_solicitacoes, name='solicitacoes_lista'),
    path('solicitacoes/<int:id>/', views.detalhe_solicitacao, name='detalhe_solicitacao'),

    path('orcamento/criar/<int:solicitacao_id>/', views.criar_orcamento, name='criar_orcamento'),
]
