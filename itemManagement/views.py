from django.shortcuts import render, redirect

# Create your views here.
from itemManagement.models import Item, Location, ItemStorage, Photo, Location


def homePage(request):

    context = {
        'items': [
            item.getItemSummary() for item in Item.objects.all()
        ]
    }

    return render(request, 'itemManagement/homepage.html', context=context)


def sampleItem(request, itemId):
    print(f"Item ID requested: {itemId}")

    context = Item.objects.filter(id=itemId).first().getItemDetails()
    return render(request, 'itemManagement/item_details.html', context=context)


def locationList(request):
    locations = Location.objects.all().order_by('name')
    return render(request, 'itemManagement/locations.html', {'locations': locations})

