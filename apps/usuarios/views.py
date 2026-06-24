from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import RegistroForm
from .models import Perfil


@transaction.atomic
def registro(request):

    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]

            user.save()

            Perfil.objects.create(
                user=user,
                telefono=form.cleaned_data["telefono"],
                es_comprador=True,
                es_vendedor=True,
            )

            login(request, user)

            messages.success(
                request,
                "Tu cuenta fue creada correctamente. "
                "Ya podés comprar y publicar propiedades.",
            )

            return redirect("inicio")

        messages.error(
            request,
            "No se pudo crear la cuenta. " "Revisá los campos marcados.",
        )

        print("ERRORES DEL REGISTRO:")
        print(form.errors)

    else:
        form = RegistroForm()

    return render(
        request,
        "registration/registro.html",
        {
            "form": form,
        },
    )
