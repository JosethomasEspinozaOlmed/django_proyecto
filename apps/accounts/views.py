from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
