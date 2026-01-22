from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inclui as rotas do app pages na raiz do site
    path('pages/', include('pages.urls')),
]
