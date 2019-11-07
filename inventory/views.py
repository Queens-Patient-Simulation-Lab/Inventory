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
