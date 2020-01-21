from django.shortcuts import render
from itemManagement.models import Item


def InventoryOnHand(request):
    data = [{"name": x.title, "total": x.totalQuantity} for x in Item.objects.all()]
    data = sorted(data, key = lambda x: x["name"])
    return render(request, 'onHand.html', {"items": data})