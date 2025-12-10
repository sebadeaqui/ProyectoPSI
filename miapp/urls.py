from django.urls import path
from . import views

urlpatterns = [
    path("", views.primeravista, name="principal"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("registro/", views.formulario, name="formulario"),
    path("gestion/", views.segundavista, name="gestion"),
    path("modificar/", views.modificar_menu, name="modificar"),
]