from django.urls import path
from .views import *

urlpatterns = [
    path("login/", verificar_login, name="verificar_login"),
    path("estoque/", listar_imoveis, name="listar_imoveis"),
    path("estoque/disponivel/", listar_imoveis, {'disponivel': True}, name="listar_imoveis_disponiveis"),
    path("estoque/<int:id>/", getImovelPorId, name="getImovelPorId"),
    path("usuario/", carregar_usuario, name="carregar_usuario"),
    path("deslogar/", deslogar, name='deslogar'),
    path("estoque/cadastrar/", cadastrar_imovel, name="cadastrar_imovel"),
    path("atendimentos/", listar_atendimentos, name="listar_atendimentos"),
]
