from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inclui as rotas do app pages na raiz do site
    path('pages/', include('pages.urls')),
]

handler403 = 'pages.views.erro_403' # Define a view personalizada para erros 403 (acesso negado)