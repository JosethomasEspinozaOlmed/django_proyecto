from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegistroForm
from .models import Perfil

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Perfil.objects.create(
                user=user,
                telefono=form.cleaned_data['telefono'],
                rol=form.cleaned_data['rol']
            )

            login(request, user)
            return redirect('/')
    else:
        form = RegistroForm()

    return render(request, 'registration/registro.html', {'form': form})