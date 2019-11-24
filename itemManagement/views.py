from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.


@xframe_options_exempt
def homePage(request):
    return render(request, 'itemManagement/homepage.html')




@xframe_options_exempt
def sampleItem(request):
    return render(request, 'itemManagement/sample-item.html')
