from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.


@xframe_options_exempt
def homePage(request):
    itemOne = {
        'images': ['itemManagement/nacl.jpg'],
        'name': "NaCl 0.9% 500ml",
        'locations': ['Main Storage Area'],
        'totalQuantity': 15
    }
    itemTwo = {
        'images': ['itemManagement/puppy.jpeg'],
        'name': "Puppy",
        'locations': ['Kennel'],
        'totalQuantity': 385
    }
    itemThree = {
        'images': ['itemManagement/puppy2.jpeg'],
        'name': "Puppy 2",
        'locations': ['Kennel'],
        'totalQuantity': 50
    }
    context = {
        'items': [itemOne, itemTwo, itemThree]
    }

    return render(request, 'itemManagement/homepage.html', context=context)

@xframe_options_exempt
def sampleItem(request):
    return render(request, 'itemManagement/sample-item.html')
