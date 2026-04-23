from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Propiedad
from .forms import PropiedadForm
from django.contrib import messages
from apps.usuarios.models import Perfil

def inicio(request):
    propiedades = Propiedad.objects.filter(estado='activa').order_by('-creado')

    busqueda = request.GET.get('busqueda')
    tipo = request.GET.get('tipo')

    if busqueda:
        propiedades = propiedades.filter(ciudad__icontains=busqueda) | propiedades.filter(barrio__icontains=busqueda)

    if tipo:
        propiedades = propiedades.filter(tipo=tipo)

    return render(request, 'propiedades/lista.html', {
        'propiedades': propiedades,
        'busqueda': busqueda,
        'tipo': tipo,
    })

def detalle_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    return render(request, 'propiedades/detalle.html', {'propiedad': propiedad})

@login_required
def crear_propiedad(request):
    try:
        perfil = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        return HttpResponse("Este usuario no tiene perfil creado.")

    if perfil.rol != 'vendedor':
        return HttpResponse("Solo los vendedores pueden publicar propiedades.")

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.vendedor = request.user
            propiedad.save()
            messages.success(request, "Propiedad publicada correctamente.")
            return redirect('inicio')
    else:
        form = PropiedadForm()

    return render(request, 'propiedades/crear.html', {'form': form})

@login_required
def mis_publicaciones(request):
    propiedades = Propiedad.objects.filter(vendedor=request.user).order_by('-creado')
    return render(request, 'propiedades/mis_publicaciones.html', {'propiedades': propiedades})

@login_required
def editar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk, vendedor=request.user)

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES, instance=propiedad)
        if form.is_valid():
            form.save()
            messages.success(request, "Propiedad editada correctamente.")
            return redirect('mis_publicaciones')
    else:
        form = PropiedadForm(instance=propiedad)

    return render(request, 'propiedades/editar.html', {'form': form, 'propiedad': propiedad})

@login_required
def eliminar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk, vendedor=request.user)

    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, "Propiedad eliminada correctamente.")
        return redirect('mis_publicaciones')

    return render(request, 'propiedades/eliminar.html', {'propiedad': propiedad})