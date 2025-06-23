from django.urls import path
from . import views

from .views import CustomLoginView, perfil_usuario
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('perfil/', perfil_usuario, name="perfil_usuario"),
    path("favoritos/", views.lista_favoritos, name="lista_favoritos"),

]



