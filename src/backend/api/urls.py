from django.urls import path

from .views import verificar_login

urlpatterns = [
    path("login/", verificar_login, name="verificar_login"),
]
