from . import views
from django.urls import path

urlpatterns = [
    # As seguintes rotas são para as páginas públicas do site, acessíveis a todos os usuários.
    path('', views.home, name='home'),
    path('contato/', views.contato, name='contato'),
    path('sobre/', views.sobre, name='sobre'),
    path('ajuda/', views.ajuda, name='ajuda'),

    # As seguintes rotas são para a área de mensagens, que são restritas a usuários autenticados.
    path('mensagens/', views.mensagens, name='mensagens'),

    # As seguintes rotas são para a área de pessoas, que é restrita a usuários autenticados.
    path('pessoas/', views.pessoas, name='pessoas'),
    path('pessoas/nova/', views.pessoa_create, name='pessoa_create'),
    path('pessoas/<int:pessoa_id>/editar/', views.pessoa_update, name='pessoa_update'),
    path('pessoas/<int:pessoa_id>/excluir/', views.pessoa_delete, name='pessoa_delete'),

    # As seguintes rotas são para a autenticação de usuários.
    path('restrita/', views.area_restrita, name='area_restrita'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
