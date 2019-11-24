from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
@xframe_options_exempt
def login(request):
    print(request.method)
    if (request.method == 'POST'):
        return redirect('homepage')
    else:
        return render(request, 'inventory/login.html')

@xframe_options_exempt
def homePage(request):
    return render(request, 'inventory/homepage.html')

@xframe_options_exempt
def sampleReport(request):
    return render(request, 'inventory/report_sample.html')


@xframe_options_exempt
def sampleItem(request):
    return render(request, 'inventory/sample-item.html')
