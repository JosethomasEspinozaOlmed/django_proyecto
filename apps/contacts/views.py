from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from apps.properties.models import Property
from .forms import ContactForm
from .models import ContactMessage


def contact_property(request, pk):
    property = get_object_or_404(Property, pk=pk, status='active')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.property = property
            msg.save()

            # Enviar email al vendedor
            try:
                send_mail(
                    subject=f'[InmueblesP Y] Nuevo interesado en: {property.title}',
                    message=(
                        f'Nombre: {msg.sender_name}\n'
                        f'Email: {msg.sender_email}\n'
                        f'Teléfono: {msg.sender_phone}\n\n'
                        f'Mensaje:\n{msg.message}\n\n'
                        f'Propiedad: {property.title}\n'
                        f'URL: {request.build_absolute_uri(property.get_absolute_url())}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[property.seller.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                '¡Mensaje enviado! El vendedor se contactará a la brevedad.'
            )
            return redirect('properties:detail', pk=property.pk)
    else:
        form = ContactForm()

    return render(request, 'contacts/contact.html', {
        'form': form,
        'property': property,
    })
