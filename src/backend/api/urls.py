from django.urls import path
from .views import *

urlpatterns = [
    path("login/", verificar_login, name="verificar_login"),
    path("imoveis/", listar_imoveis, name="listar_imoveis"),
]
