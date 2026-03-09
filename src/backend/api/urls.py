from django.urls import path
from .views import *

urlpatterns = [
    path("login/", verificar_login, name="verificar_login"),
    path("imoveis/", listar_imoveis, name="listar_imoveis"),
    path("usuario/", carregar_usuario, name="carregar_usuario"),
    path("deslogar/", deslogar, name='deslogar')
]
