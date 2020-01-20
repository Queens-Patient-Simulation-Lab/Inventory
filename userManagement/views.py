from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import notificationUpdateForm


# Create your views here.


def settings(request):
    return render(request, 'userManagement/settings.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings-home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userManagement/change_password.html', {'form': form})


def notification(request):
    if request.method == 'POST':
        n_form = notificationUpdateForm(request.POST, instance=request.user)
        if n_form.is_valid():
            n_form.save()
            messages.success(request, 'Your notification status was successfully updated!')
            return redirect('settings-home')
    else:
        n_form = notificationUpdateForm(instance=request.user)

    return render(request, 'userManagement/notification.html', {'n_form': n_form})
