from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.


@xframe_options_exempt
def login(request):
    print(request.method)
    if (request.method == 'POST'):
        return redirect('homepage')
    else:
        return render(request, 'security/login.html')