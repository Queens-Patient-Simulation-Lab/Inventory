from django.shortcuts import render
from itemManagement.models import Item
import csv
from django.http import HttpResponse
from datetime import date

def MainPage(request):
    return render(request, 'main.html')

def __CSVResponseGenerator(filename, header, rows):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    writer = csv.writer(response)
    writer.writerow(header)
    writer.writerows(rows)
    return response

def __GetFormattedDate():
    return date.today().strftime("%Y-%m-%d")

def CycleCount(request, format=None):
    data = []
    items = map(lambda x: x.getItemDetails(),Item.objects.all().order_by("title"))
    if format == "csv":
        for item in items:
            for location in item["locations"]:
                data.append([item["name"], location["name"], location["quantity"]])
        return __CSVResponseGenerator("CycleCount-" + __GetFormattedDate(), ["Name", "Location", "Quantity"], data)
    else:
        for item in items:
            locations = [{"location": x["name"], "quantity": x["quantity"]} for x in item["locations"]]
            data.append({"name": item["name"], "locations": locations})
        return render(request, 'cycle.html', {"items": data})

def InventoryOnHand(request, format=None):
    data = [{"name": x.title, "total": x.totalQuantity} for x in Item.objects.all().order_by("title")]
    if format == "csv":
        return __CSVResponseGenerator("Inventory-on-Hand-" + __GetFormattedDate(), ["Name", "Count"], [[x["name"], x["total"]] for x in data]) 
    else:
        return render(request, 'onHand.html', {"items": data})