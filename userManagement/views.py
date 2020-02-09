from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from .forms import notificationUpdateForm, userCreationForm
from security.models import User


# Create your views here.


def settings(request):
    if request.method == 'POST':
        p_form = PasswordChangeForm(request.user, request.POST)
        n_form = notificationUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and 'changePassword' in request.POST:
            user = p_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings-home')
        elif n_form.is_valid() and 'notification' in request.POST:
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


def userAccount(request):
    if request.method == 'POST':
        c_form = userCreationForm(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, 'Account was successfully created!')
            return redirect('user-account')
    else:
        c_form = userCreationForm(request.POST)

    context = {
        'staff': User.objects.all(),
        'c_form': c_form,
    }

    return render(request, 'userManagement/userAccount.html', context)


def userRegister(request):
    if request.method == 'POST':
        c_form = userCreationForm(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, 'Account was successfully created!')
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
    u.groups.all().delete()
    u.deleteFlag = True
    u.save()
    messages.success(request, 'Account was successfully deleted!')

    return redirect('user-account')

def userRole(request, email):
    u = User.objects.filter(email=email).first()
    admin = Group.objects.get(name="admin")
    labAssistance = Group.objects.get(name="labAssistance")
    if u.is_superuser:
        u.is_superuser = False
        admin.user_set.remove(u)
        labAssistance.user_set.add(u)
    else:
        u.is_superuser = True
        labAssistance.user_set.remove(u)
        admin.user_set.add(u)
    u.save()
    messages.success(request, 'Account role was successfully changed!')

    return redirect('user-account')