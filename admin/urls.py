"""
URL configuration for admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from store import views, cadastros, pdv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cadastros/', views.cadastros, name='cadastros'),
    path('cadastros_clientes/', cadastros.cadastros_clientes, name='cadastros_clientes'),
    path('cadastro_categorias/', cadastros.cadastro_categorias, name='cadastro_categorias'),
    path('cadastro_produtos/', cadastros.cadastro_produtos, name='cadastro_produtos'),
    path('estoque/', views.estoque, name='estoque'),
    path('pdv/', views.pdv, name='pdv'),
    path('buscar_produtos_pdv/', views.buscar_produtos_pdv, name='buscar_produtos_pdv'),
    path('finalizar_compra/', pdv.finalizar_compra, name='finalizar_compra'),
    ]