from django.shortcuts import render

# Create your views here.

def locationList(request):
    return render(request, 'locations.html')