from django.shortcuts import render
from itemManagement.models import Item

def MainPage(request):
    return render(request, 'main.html')


def CycleCount(request):
    data = []
    for item in Item.objects.all():
        item = item.getItemDetails()
        locations = [{"location": x["name"], "quantity": x["quantity"]} for x in item["locations"]]
        data.append({"name": item["name"], "locations": locations})
    data = sorted(data, key = lambda x: x["name"])
    return render(request, 'cycle.html', {"items": data})

def InventoryOnHand(request):
    data = [{"name": x.title, "total": x.totalQuantity} for x in Item.objects.all()]
    data = sorted(data, key = lambda x: x["name"])
    return render(request, 'onHand.html', {"items": data})