from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
from itemManagement.models import Item, Location, ItemStorage, Photo


@xframe_options_exempt
def homePage(request):

    context = {
        'items': [
            item.getItemSummary() for item in Item.objects.all()
        ]
    }

    return render(request, 'itemManagement/homepage.html', context=context)


@xframe_options_exempt
def sampleItem(request, itemId):
    print(f"Item ID requested: {itemId}")

    context = Item.objects.get(id=itemId).getItemDetails()
    return render(request, 'itemManagement/item_details.html', context=context)
