# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, CustomLoginForm
from django.contrib import messages
from books.models import Book,Favorite

from django.contrib.auth.views import LoginView

def registro(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu cuenta ha sido creada. Ahora puedes iniciar sesión.")
            return redirect("login")
    else:
        form = RegistroUsuarioForm()
    return render(request, "users/registro.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomLoginForm


@login_required
def perfil_usuario(request):
    return render(request, "users/perfil.html")


@login_required
def lista_favoritos(request):
    favoritos = Favorite.objects.filter(user=request.user).select_related('book')
    libros = [fav.book for fav in favoritos]
    
    return render(request, "users/favoritos.html", {"libros": libros})


