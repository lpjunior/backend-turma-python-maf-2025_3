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
    path("feedback/<uuid:token>/", views.feedback_publico, name="feedback_publico"),
    # ========================
    #   Area administrativa
    # ========================
    path('gestao/', views.dashboard, name='dashboard'),

    # ========================
    #   Gestão de Clientes
    # ========================
    path('gestao/clientes', views.clientes, name='clientes'),
    path('gestao/cliente/novo/', views.cliente_create, name='cliente_create'),
    path('gestao/cliente/<int:cliente_id>', views.cliente_detalhe, name='cliente_detalhe'),
    path('gestao/cliente/<int:cliente_id>/editar', views.cliente_update, name='cliente_update'),
    path('gestao/cliente/<int:cliente_id>/excluir', views.cliente_delete, name='cliente_delete'),

    # ========================
    #   Gestão de Projetos
    # ========================
    path('gestao/projetos/', views.projetos_admin, name='projetos_admin'),
    path('gestao/projetos/novo', views.projeto_create, name='projeto_create'),
    path('gestao/projetos/<int:projeto_id>/editar', views.projeto_update, name='projeto_update'),
    path('gestao/projetos/<int:projeto_id>/excluir', views.projeto_delete, name='projeto_delete'),

    # ========================
    #   Gestão de Solicitações
    # ========================
    path('gestao/solicitacoes/', views.lista_solicitacoes, name='solicitacoes'),
    path('gestao/solicitacoes/<int:solicitacao_id>/', views.solicitacao_detalhe, name='solicitacao_detalhe'),
    path('gestao/solicitacoes/<int:solicitacao_id>/orcamento', views.criar_orcamento, name='criar_orcamento'),

    # ========================
    #   Gestão de Depoimentos
    # ========================
    path("gestao/solicitacoes/<int:solicitacao_id>/solicitar-depoimento/", views.solicitar_depoimento, name="solicitar_depoimento"),
    path("gestao/depoimentos/", views.depoimentos_admin, name="depoimentos_admin"),
    path("gestao/depoimentos/<int:depoimento_id>/moderar/", views.depoimento_moderar, name="depoimento_moderar"),
]