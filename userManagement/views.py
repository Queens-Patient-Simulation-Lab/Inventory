from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.utils.encoding import force_text, smart_bytes

from emails.email import EmailManager as em
from django.contrib.auth.tokens import default_token_generator
from .forms import notificationUpdateForm, userCreationForm
from security.models import User
from logs.models import UserLogs
import logs.models as Logs
from global_login_required import login_not_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# Create your views here.
def settings(request):
    if request.method == 'POST':
        p_form = PasswordChangeForm(request.user, request.POST)  # change password form
        n_form = notificationUpdateForm(request.POST, instance=request.user) # change notification status form

        if p_form.is_valid() and 'changePassword' in request.POST:
            user = p_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings-home')
        elif n_form.is_valid() and 'notification' in request.POST:
            n_form.save()
            messages.success(request, 'Your notification status was successfully updated!')
            UserLogs.logging(operator_user=request.user, logCode=Logs.LOGCODE_100003, logMsg=Logs.LOGMSG_100003)
            return redirect('settings-home')
    else:
        p_form = PasswordChangeForm(request.user)
        n_form = notificationUpdateForm(instance=request.user) # instance: is to get the current user's notification status

    context = {
        "n_form": n_form,
        "p_form": p_form,
    }
    return render(request, 'userManagement/settings.html', context)


def userAccount(request):
    # admin only page
    if request.method == 'GET':
        if not request.user.is_superuser:
            return render(request, "security/403.html", status=403)

    if request.method == 'POST':
        email = request.POST.get('email', "").strip()
        try:
            validate_email(email)

            if User.objects.filter(email=email).exists():
                messages.error(request, f'Email has already existed')
                redirect('user-account')
            else:
                emailed_user = User.objects.create_user(email=email,
                                                        password='haveNotSetPassword',
                                                        name='waiting for invitation acceptance')
                emailed_user.save()
                em.sendAccountSetupEmail(user=emailed_user,
                                         uidb64=urlsafe_base64_encode(smart_bytes(emailed_user.pk)),
                                         token=default_token_generator.make_token(emailed_user))
                messages.success(request, f'Invitation email has been sent.')
                redirect('user-account')
        except ValidationError:
            messages.error(request, f'Incorrect email format, please enter correct email again.')
            redirect('user-account')

    context = {
        'staff': User.objects.filter(deleteFlag=False),
    }

    return render(request, 'userManagement/userAccount.html', context)


@login_not_required
def userRegister(request, uidb64 ,token):
    assert uidb64 is not None and token is not None
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            c_form = userCreationForm(request.POST, instance=user)
            if c_form.is_valid():
                c_form.save()
                messages.success(request, f'Account ({user.email}) has successfully been created!')
                UserLogs.logging(operator_user=user, logCode=Logs.LOGCODE_100001, logMsg=Logs.LOGMSG_100001)
                return render(request, 'security/login.html')
        else:
            c_form = userCreationForm()
    else:
        messages.error(request, f'Authentication Failure')
        return render(request, 'security/403.html', status=403)

    context = {
        'c_form': c_form,
    }

    return render(request, 'userManagement/userRegister.html', context)


@login_not_required
def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email', "").strip()
        try:
            validate_email(email)

            emailed_user = User.objects.filter(email=email).first()
            if emailed_user:
                em.sendPasswordResetEmail(user=emailed_user,
                                         uidb64=urlsafe_base64_encode(smart_bytes(emailed_user.pk)),
                                         token=default_token_generator.make_token(emailed_user))
                messages.success(request, f'Password reset email has been sent.')
                redirect('forget-password')
            else:
                messages.error(request, f'Account with this email does not exist')
                redirect('forget-password')
        except ValidationError:
            messages.error(request, f'Incorrect email format, please enter correct email again.')
            redirect('forget-password')

    return render(request, 'userManagement/forgetPassword.html')


@login_not_required
def forgetPasswordConfirm(request, uidb64, token):
    assert uidb64 is not None and token is not None
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Password has successfully been reseted!')
                return render(request, 'security/login.html')
        else:
            form = SetPasswordForm(user)
    else:
        messages.error(request, f'Authentication Failure')
        return render(request, 'security/403.html', status=403)

    context = {
        'form': form,
    }

    return render(request, 'userManagement/forgetPasswordConfirm.html', context)


def userDelete(request, email):
    u = User.objects.filter(email=email).first()
    u.deleteFlag = True
    u.save()
    messages.success(request, f'Account {email} was successfully deleted!')
    UserLogs.logging(operator_user=request.user, target_user=u, logCode=Logs.LOGCODE_100002, logMsg=Logs.LOGMSG_100002)
    return redirect('user-account')


# change user role to admin
def userAdmin(request, email):
    u = User.objects.filter(email=email).first()
    u.is_superuser = True
    u.save()
    messages.success(request, f'{email}\'s account role was successfully changed!')
    UserLogs.logging(operator_user=request.user, target_user=u, logCode=Logs.LOGCODE_100005, logMsg=Logs.LOGMSG_100005)
    return redirect('user-account')


# change user role to lab assistant
def userLabAssistant(request, email):
    u = User.objects.filter(email=email).first()
    u.is_superuser = False
    u.save()
    messages.success(request, f'{email}\'s account role was successfully changed!')
    UserLogs.logging(operator_user=request.user, target_user=u, logCode=Logs.LOGCODE_100006, logMsg=Logs.LOGMSG_100006)
    return redirect('user-account')