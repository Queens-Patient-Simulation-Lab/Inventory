from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib import auth, messages

# Create your views here.
from django.views.generic import TemplateView
from global_login_required import login_not_required

from security.models import User


@login_not_required
class LoginView(TemplateView):
    def get(self, request):
        if (request.user.is_authenticated):
            return redirect('homepage')
        return render(request, 'security/login.html')

    def post(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', "")

        if len(email.strip()) == 0:
            messages.error(request, "Email cannot be empty.")
            return redirect('login')
        if len(password.strip()) == 0:
            messages.error(request, "Password cannot be empty.")
            return redirect('login')

        user = auth.authenticate(request, username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Invalid Credentials.")
            return redirect('login')


def logout(request):
    auth.logout(request)
    return redirect('login')


@login_not_required
def handler403(request, *args, **argv):
    return render(request, 'security/404.html', status=404)


@login_not_required
def handler404(request, *args, **argv):
    return render(request, 'security/404.html', status=404)


@login_not_required
def handler500(request, *args, **argv):
    return render(request, 'security/500.html', status=500)