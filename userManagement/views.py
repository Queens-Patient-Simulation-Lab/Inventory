from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import notificationUpdateForm, userCreationForm
from global_login_required import login_not_required
from security.models import User
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def settings(request):
    logger.warning(f"settings page")
    if request.method == 'POST':
        p_form = PasswordChangeForm(request.user, request.POST)
        n_form = notificationUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and 'changePassword' in request.POST:
            user = p_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            logger.debug(f"changed password")
            return redirect('settings-home')
        elif n_form.is_valid() and 'notification' in request.POST:
            n_form.save()
            messages.success(request, 'Your notification status was successfully updated!')
            logger.debug(f"changed notification status")
            return redirect('settings-home')
    else:
        p_form = PasswordChangeForm(request.user)
        n_form = notificationUpdateForm(instance=request.user)

    context = {
        "n_form": n_form,
        "p_form": p_form,
    }
    return render(request, 'userManagement/settings.html', context)


def userAccount(request):
    if request.method == 'GET':
        if not request.user.is_superuser:
            return render(request, "security/403.html", status=403)

    if request.method == 'POST':
        c_form = userCreationForm(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, f'Account was successfully created!')
            return redirect('user-account')
    else:
        c_form = userCreationForm(request.POST)

    context = {
        'staff': User.objects.filter(deleteFlag=False),
        'c_form': c_form,
    }

    return render(request, 'userManagement/userAccount.html', context)

#TODO The page is to create a user account when user clicks the link in the invitation email
def userRegister(request):
    if request.method == 'POST':
        c_form = userCreationForm(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, f'Account was successfully created!')
            return redirect('user-account')
    else:
        c_form = userCreationForm(request.POST)

    context = {
        'staff': User.objects.all(),
        'c_form': c_form,
    }

    return render(request, 'userManagement/userAccount.html', context)


def userDelete(request, email):
    u = User.objects.filter(email=email).first()
    u.deleteFlag = True
    u.save()
    messages.success(request, f'Account {email} was successfully deleted!')

    return redirect('user-account')


def userAdmin(request, email):
    u = User.objects.filter(email=email).first()
    u.is_superuser = True
    u.save()
    messages.success(request, f'{email}\'s account role was successfully changed!')

    return redirect('user-account')


def userLabAssistant(request, email):
    u = User.objects.filter(email=email).first()
    u.is_superuser = False
    u.save()
    messages.success(request, f'{email}\'s account role was successfully changed!')

    return redirect('user-account')