from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib import auth

# Create your views here.
from global_login_required import login_not_required

from security.models import User


@xframe_options_exempt
@login_not_required
def login(request):
    if (request.user.is_authenticated):
        return redirect('homepage')

    # just for now, we create a default user if it doesn't exist
    user = User.objects.filter(email="test@test.com").first()
    if not user:
        print("Making new user")
        user = User.objects.create_user("test@test.com", "abcd")
        assert user.password != "abcd"

    if (request.method == 'POST'):
        email = request.POST.get('email', '')
        password = request.POST.get('password', "")
        # todo: field validation
        user = auth.authenticate(request, username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('homepage')
        else:
            return redirect('login')
    else:
        return render(request, 'security/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')
