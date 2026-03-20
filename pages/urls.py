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
    path('contato/', views.contato, name='contato'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ========================
    #   Area administrativa
    # ========================
    path('gestao/', views.dashboard, name='dashboard'),
    path('gestao/clientes', views.clientes, name='clientes'),
    path('gestao/cliente/novo/', views.cliente_create, name='cliente_create'),
    path('gestao/cliente/<int:id_cliente>', views.cliente_detalhe, name='cliente_detalhe'),
    path('gestao/cliente/<int:id_cliente>/editar', views.cliente_update, name='cliente_update'),
    path('gestao/cliente/<int:id_cliente>/excluir', views.cliente_delete, name='cliente_delete'),

    path('gestao/solicitacoes/', views.lista_solicitacoes, name='lista_solicitacoes'),
    path('gestao/solicitacoes/<int:solicitacao_id>/', views.detalhe_solicitacao, name='detalhe_solicitacao'),

    path('gestao/solicitacoes/<int:solicitacao_id>/orcamento', views.criar_orcamento, name='criar_orcamento'),
]
