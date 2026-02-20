from . import views
from django.urls import path

urlpatterns = [
    # As seguintes rotas são para as páginas públicas do site, acessíveis a todos os usuários.
    path('', views.home, name='home'),
    path('contato/', views.contato, name='contato'),
    path('sobre/', views.sobre, name='sobre'),
    path('ajuda/', views.ajuda, name='ajuda'),
    path('ola/<str:nome>/<int:idade>', views.saudacao, name='saudacao'),

    # As seguintes rotas são para a área de mensagens e pessoas, que são restritas a usuários autenticados.
    path('mensagens/', views.mensagens, name='mensagens'),
    path('pessoas/', views.pessoas, name='pessoas'),

    # As seguintes rotas são para a autenticação de usuários.
    path('restrita/', views.area_restrita, name='area_restrita'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
