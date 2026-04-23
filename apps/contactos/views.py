from django.shortcuts import render, redirect, get_object_or_404
from apps.propiedades.models import Propiedad
from .forms import ContactoForm
from django.contrib import messages

def contactar_vendedor(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.propiedad = propiedad
            contacto.save()
            messages.success(request, "Mensaje enviado correctamente al vendedor.")
            return redirect('detalle_propiedad', pk=propiedad.pk)
    else:
        form = ContactoForm()

    return render(request, 'contactos/contactar.html', {
        'form': form,
        'propiedad': propiedad
    })