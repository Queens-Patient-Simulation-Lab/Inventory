from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def login(request):
    print(request.method)
    if (request.method == 'POST'):
        return redirect('inventory-homepage')
    else:
        return render(request, 'inventory/login.html')

def homePage(request):
    return render(request, 'inventory/homepage.html')

def sampleReport(request):
    return render(request, 'inventory/report_sample.html')


def sampleItem(request):
    return render(request, 'inventory/sample-item.html')
