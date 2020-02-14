from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib import auth
from django.template import RequestContext

# Create your views here.
from global_login_required import login_not_required

from security.models import User


@xframe_options_exempt
@login_not_required
def login(request):
    if (request.user.is_authenticated):
        return redirect('homepage')

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


def handler403(request, *args, **argv):
    response = render_to_response('security/403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response


def handler404(request, *args, **argv):
    return render(request, 'security/404.html', status=404)


def handler500(request, *args, **argv):
    return render(request, 'security/500.html', status=500)