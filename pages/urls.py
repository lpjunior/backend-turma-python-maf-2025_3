from . import views
from django.urls import path

urlpatterns = [
    # Quando acessar a raiz do site ("/"), chama a view home
    path('', views.home, name='home'),
    path('contato/', views.contato, name='contato'),
    path('ola/<str:nome>/<int:idade>', views.saudacao, name='saudacao'),
]