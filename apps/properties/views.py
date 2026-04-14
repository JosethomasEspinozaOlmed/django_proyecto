from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from apps.contacts.forms import ContactForm
from .models import Property, City
from .filters import PropertyFilter
from .forms import PropertyForm, PropertyPhotoFormSet


def property_list(request):
    qs = Property.objects.filter(status='active').select_related('city', 'seller').prefetch_related('photos')
    f = PropertyFilter(request.GET, queryset=qs)
    paginator = Paginator(f.qs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'properties/list.html', {
        'filter': f,
        'page_obj': page_obj,
        'total_count': f.qs.count(),
    })


def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    Property.objects.filter(pk=pk).update(views_count=prop.views_count + 1)
    related = Property.objects.filter(
        city=prop.city, status='active'
    ).exclude(pk=pk).select_related('city').prefetch_related('photos')[:3]
    return render(request, 'properties/detail.html', {
        'property': prop,
        'related': related,
        'contact_form': ContactForm(),
    })


@login_required
def property_create(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_seller:
        messages.error(request, 'Solo los vendedores pueden publicar propiedades. Actualizá tu perfil.')
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = PropertyForm(request.POST)
        formset = PropertyPhotoFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            property = form.save(commit=False)
            property.seller = request.user
            property.save()
            formset.instance = property
            formset.save()
            messages.success(request, '¡Propiedad publicada correctamente!')
            return redirect('properties:detail', pk=property.pk)
    else:
        form = PropertyForm()
        formset = PropertyPhotoFormSet()

    return render(request, 'properties/form.html', {
        'form': form,
        'formset': formset,
        'title': 'Publicar propiedad',
    })


@login_required
def property_edit(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if property.seller != request.user:
        return HttpResponseForbidden('No tenés permiso para editar esta propiedad.')

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        formset = PropertyPhotoFormSet(request.POST, request.FILES, instance=property)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Propiedad actualizada correctamente.')
            return redirect('properties:detail', pk=property.pk)
    else:
        form = PropertyForm(instance=property)
        formset = PropertyPhotoFormSet(instance=property)

    return render(request, 'properties/form.html', {
        'form': form,
        'formset': formset,
        'property': property,
        'title': 'Editar propiedad',
    })


@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if property.seller != request.user:
        return HttpResponseForbidden('No tenés permiso para eliminar esta propiedad.')
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Propiedad eliminada.')
        return redirect('properties:my_properties')
    return render(request, 'properties/confirm_delete.html', {'property': property})


@login_required
def my_properties(request):
    properties = Property.objects.filter(seller=request.user).select_related('city').prefetch_related('photos')
    return render(request, 'properties/my_properties.html', {'properties': properties})
