from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import notificationUpdateForm


# Create your views here.


def settings(request):
    if request.method == 'POST':
        p_form = PasswordChangeForm(request.user, request.POST)
        n_form = notificationUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid():
            user = p_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings-home')
        if n_form.is_valid():
            n_form.save()
            messages.success(request, 'Your notification status was successfully updated!')
            return redirect('settings-home')
    else:
        p_form = PasswordChangeForm(request.user)
        n_form = notificationUpdateForm(instance=request.user)

    context = {
        "n_form": n_form,
        "p_form": p_form,
    }
    return render(request, 'userManagement/settings.html', context)
