# users/views.py
from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm, CustomLoginForm
from django.contrib import messages

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
    
