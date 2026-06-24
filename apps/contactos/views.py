from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from apps.propiedades.models import Propiedad
from apps.usuarios.models import Perfil

from .forms import ContactoForm
from .models import Contacto


@login_required
def contactar_vendedor(request, pk):
    propiedad = get_object_or_404(
        Propiedad,
        pk=pk,
        estado="activa",
    )

    perfil, creado = Perfil.objects.get_or_create(
        user=request.user,
        defaults={
            "telefono": "",
            "es_comprador": True,
            "es_vendedor": True,
        },
    )

    if not perfil.es_comprador:
        messages.error(
            request,
            "Tu cuenta no tiene habilitado " "el rol de comprador.",
        )

        return redirect(
            "detalle_propiedad",
            pk=propiedad.pk,
        )

    if propiedad.vendedor_id == request.user.id:
        messages.warning(
            request,
            "No podés enviarte un mensaje " "a tu propia publicación.",
        )

        return redirect(
            "detalle_propiedad",
            pk=propiedad.pk,
        )

    contacto_inicial = perfil.telefono or request.user.email

    if request.method == "POST":
        formulario = ContactoForm(request.POST)

        if formulario.is_valid():
            contacto = formulario.save(commit=False)

            contacto.propiedad = propiedad
            contacto.comprador = request.user

            contacto.nombre = request.user.get_full_name() or request.user.username

            contacto.save()

            messages.success(
                request,
                "Tu mensaje fue enviado " "al vendedor.",
            )

            return redirect(
                "detalle_propiedad",
                pk=propiedad.pk,
            )

    else:
        formulario = ContactoForm(
            initial={
                "contacto": contacto_inicial,
            }
        )

    return render(
        request,
        "contactos/contactar.html",
        {
            "form": formulario,
            "propiedad": propiedad,
        },
    )


@login_required
def mensajes_recibidos(request):
    mensajes_contacto = Contacto.objects.filter(
        propiedad__vendedor=request.user
    ).select_related(
        "propiedad",
        "comprador",
    )

    return render(
        request,
        "contactos/mensajes_recibidos.html",
        {
            "mensajes_contacto": (mensajes_contacto),
        },
    )
