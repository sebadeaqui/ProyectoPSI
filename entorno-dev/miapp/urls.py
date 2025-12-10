from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.saludo, name="vistaPrincipal"),
    path("pestana/", views.pestana),
    path("cachorro/", views.cachorro),
    path("principal/", views.primeravista),
    path("secundaria/", views.segundavista, name="vistaSecundaria"),
    path("formulario/", views.formulario, name="formulario"),
    path("login/", views.login, name="login"),
    
    # NUEVAS RUTAS
    path("usuarios/", views.usuarios_registrados, name="usuarios_registrados"),
    path("eliminar/<int:id>/", views.eliminar_usuario, name="eliminar_usuario"),
    path("actualizar/<int:id>/", views.actualizar_usuario, name="actualizar_usuario"),
    path("logout/", views.logout, name="logout"),
]