from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
from itemManagement.models import Item, Location, ItemStorage, Photo


@xframe_options_exempt
def homePage(request):
    context = {
        'items': []
    }
    for item in Item.objects.all():
        context['items'].append(
            {
                'name': item.title,
                'locations':  [x.name for x in item.locations.all()],
                'totalQuantity': item.totalQuantity,
                'images': [x.data for x in  item.photo_set.all()]
            }
        )

    return render(request, 'itemManagement/homepage.html', context=context)


@xframe_options_exempt
def sampleItem(request):
    return render(request, 'itemManagement/sample-item.html')
