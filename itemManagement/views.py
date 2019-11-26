from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
from itemManagement.models import Item, Location, ItemStorage, Photo


@xframe_options_exempt
def homePage(request):
    # itemOne = {
    #     'images': ['itemManagement/nacl.jpg'],
    #     'name': "NaCl 0.9% 500ml",
    #     'locations': ['Main Storage Area'],
    #     'totalQuantity': 15
    # }
    # itemTwo = {
    #     'images': ['itemManagement/puppy.jpeg'],
    #     'name': "Puppy",
    #     'locations': ['Kennel'],
    #     'totalQuantity': 385
    # }
    # itemThree = {
    #     'images': ['itemManagement/puppy2.jpeg'],
    #     'name': "Puppy 2",
    #     'locations': ['Kennel'],
    #     'totalQuantity': 50
    # }
    # item = Item(title="MyTITLE", locationName="Hello", totalQuantity=33).save()
    Item.objects.all().delete()
    mainStorage = Location.objects.create(name="Main Storage Area")
    kennel = Location.objects.create(name="Kennel")

    itemOne = Item.objects.create(
        title="NaCl 0.9% 500ml"
    )
    itemTwo = Item.objects.create(
        title="Puppy"
    )
    itemThree = Item.objects.create(
        title="Puppy 2"
    )

    ItemStorage.objects.create(item=itemOne, location=mainStorage,quantity=15)
    ItemStorage.objects.create(item=itemTwo, location=kennel,quantity=385)
    ItemStorage.objects.create(item=itemThree, location=kennel,quantity=50)

    Photo.objects.create(
        mimeType="jpg",
        data='itemManagement/nacl.jpg',
        order=1,
        depicts=itemOne
    )
    Photo.objects.create(
        mimeType="jpeg",
        data='itemManagement/puppy.jpeg',
        order=1,
        depicts=itemTwo
    )
    Photo.objects.create(
        mimeType="jpeg",
        data='itemManagement/puppy2.jpeg',
        order=1,
        depicts=itemThree
    )


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
