"""edital023 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, cadastro, sair, acessar, agendar, comprovante, esqueci


app_name = 'edital023'
urlpatterns = [
    path("select2/", include("django_select2.urls")),
    path('sair/', sair, name="sair"),
    path('acessar/', acessar, name="acessar"),
    path('esqueci/', esqueci, name="esqueci"),
    path('agendar/', agendar, name="agendar"),
    path('comprovante/', comprovante, name="comprovante"),
    path('cadastro/', cadastro, name="cadastro"),
    path('admin/', admin.site.urls),
    path('', home, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
