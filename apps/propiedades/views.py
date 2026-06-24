from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views.decorators.http import require_POST

from apps.usuarios.models import Perfil

from .data import (
    DEPARTAMENTOS_CIUDADES,
    get_ciudades_for_departamento,
)
from .forms import PropiedadForm
from .models import Propiedad


def obtener_perfil(user):
    perfil, creado = Perfil.objects.get_or_create(
        user=user,
        defaults={
            "telefono": "",
            "es_comprador": True,
            "es_vendedor": True,
        },
    )

    return perfil


def inicio(request):
    propiedades = Propiedad.objects.filter(estado="activa").select_related("vendedor")

    busqueda = request.GET.get(
        "busqueda",
        "",
    ).strip()

    tipo = request.GET.get(
        "tipo",
        "",
    ).strip()

    departamento = request.GET.get(
        "departamento",
        "",
    ).strip()

    moneda = request.GET.get(
        "moneda",
        "",
    ).strip()

    orden = request.GET.get(
        "orden",
        "recientes",
    ).strip()

    if busqueda:
        propiedades = propiedades.filter(
            Q(titulo__icontains=busqueda)
            | Q(ciudad__icontains=busqueda)
            | Q(barrio__icontains=busqueda)
            | Q(departamento__icontains=busqueda)
        )

    tipos_validos = dict(Propiedad.TIPO_CHOICES)

    if tipo in tipos_validos:
        propiedades = propiedades.filter(tipo=tipo)

    departamentos_validos = dict(Propiedad.DEPARTAMENTO_CHOICES)

    if departamento in departamentos_validos:
        propiedades = propiedades.filter(departamento=departamento)

    monedas_validas = dict(Propiedad.MONEDA_CHOICES)

    if moneda in monedas_validas:
        propiedades = propiedades.filter(moneda=moneda)

    tipos_orden = {
        "recientes": "-creado",
        "precio_asc": "precio",
        "precio_desc": "-precio",
    }

    propiedades = propiedades.order_by(
        tipos_orden.get(
            orden,
            "-creado",
        )
    )

    paginador = Paginator(
        propiedades,
        9,
    )

    pagina = paginador.get_page(request.GET.get("page"))

    contexto = {
        "page_obj": pagina,
        "propiedades": pagina.object_list,
        "busqueda": busqueda,
        "tipo": tipo,
        "departamento": departamento,
        "moneda": moneda,
        "orden": orden,
        "departamentos": (Propiedad.DEPARTAMENTO_CHOICES),
        "total_resultados": paginador.count,
    }

    return render(
        request,
        "propiedades/lista.html",
        contexto,
    )


def detalle_propiedad(request, pk):
    propiedad = get_object_or_404(
        Propiedad.objects.select_related("vendedor"),
        pk=pk,
    )

    usuario_es_vendedor = (
        request.user.is_authenticated and propiedad.vendedor_id == request.user.id
    )

    if propiedad.estado != "activa" and not usuario_es_vendedor:
        raise Http404("Esta publicación no está disponible.")

    return render(
        request,
        "propiedades/detalle.html",
        {
            "propiedad": propiedad,
        },
    )


@login_required
def crear_propiedad(request):
    perfil = obtener_perfil(request.user)

    if not perfil.es_vendedor:
        messages.error(
            request,
            "Tu cuenta no tiene habilitado " "el rol de vendedor.",
        )

        return redirect("inicio")

    if request.method == "POST":
        formulario = PropiedadForm(
            request.POST,
            request.FILES,
        )

        if formulario.is_valid():
            propiedad = formulario.save(commit=False)

            propiedad.vendedor = request.user
            propiedad.estado = "activa"
            propiedad.save()

            messages.success(
                request,
                "La propiedad fue publicada " "correctamente.",
            )

            return redirect("mis_publicaciones")

        messages.error(
            request,
            "Revisá los campos marcados " "antes de publicar.",
        )

    else:
        formulario = PropiedadForm()

    return render(
        request,
        "propiedades/formulario.html",
        {
            "form": formulario,
            "titulo_pagina": ("Publicar propiedad"),
            "es_edicion": False,
        },
    )


@login_required
def mis_publicaciones(request):
    perfil = obtener_perfil(request.user)

    if not perfil.es_vendedor:
        messages.error(
            request,
            "Tu cuenta no tiene habilitado " "el rol de vendedor.",
        )

        return redirect("inicio")

    propiedades = Propiedad.objects.filter(vendedor=request.user)

    return render(
        request,
        "propiedades/mis_publicaciones.html",
        {
            "propiedades": propiedades,
        },
    )


@login_required
def editar_propiedad(request, pk):
    propiedad = get_object_or_404(
        Propiedad,
        pk=pk,
        vendedor=request.user,
    )

    if request.method == "POST":
        formulario = PropiedadForm(
            request.POST,
            request.FILES,
            instance=propiedad,
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "Los cambios fueron guardados.",
            )

            return redirect("mis_publicaciones")

        messages.error(
            request,
            "Revisá los campos marcados " "antes de guardar.",
        )

    else:
        formulario = PropiedadForm(instance=propiedad)

    return render(
        request,
        "propiedades/formulario.html",
        {
            "form": formulario,
            "propiedad": propiedad,
            "titulo_pagina": ("Editar propiedad"),
            "es_edicion": True,
        },
    )


@login_required
@require_POST
def cambiar_estado_propiedad(
    request,
    pk,
):
    propiedad = get_object_or_404(
        Propiedad,
        pk=pk,
        vendedor=request.user,
    )

    if propiedad.estado == "activa":
        propiedad.estado = "pausada"
        texto_estado = "pausada"
    else:
        propiedad.estado = "activa"
        texto_estado = "activada"

    propiedad.save(update_fields=["estado"])

    messages.success(
        request,
        f"La publicación fue {texto_estado}.",
    )

    return redirect("mis_publicaciones")


@login_required
def eliminar_propiedad(request, pk):
    propiedad = get_object_or_404(
        Propiedad,
        pk=pk,
        vendedor=request.user,
    )

    if request.method == "POST":
        propiedad.delete()

        messages.success(
            request,
            "La propiedad fue eliminada.",
        )

        return redirect("mis_publicaciones")

    return render(
        request,
        "propiedades/eliminar.html",
        {
            "propiedad": propiedad,
        },
    )


def api_ciudades(request):
    departamento = request.GET.get(
        "departamento",
        "",
    )

    busqueda = (
        request.GET.get(
            "q",
            "",
        )
        .strip()
        .lower()
    )

    if departamento:
        ciudades = get_ciudades_for_departamento(departamento)
    else:
        ciudades = [
            ciudad for lista in (DEPARTAMENTOS_CIUDADES.values()) for ciudad in lista
        ]

    if busqueda:
        ciudades = [ciudad for ciudad in ciudades if busqueda in ciudad.lower()]

    ciudades_unicas = list(dict.fromkeys(ciudades))[:50]

    return JsonResponse(
        {
            "ciudades": ciudades_unicas,
        }
    )
