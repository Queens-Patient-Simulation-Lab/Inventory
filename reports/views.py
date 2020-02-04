import csv
import io
from django.shortcuts import render
from django.template.loader import render_to_string
from itemManagement.models import Item
from django.http import HttpResponse, FileResponse
from datetime import date
from weasyprint import HTML


def MainPage(request):
    return render(request, 'web/main.html')


def __CSVResponseGenerator(filenamePrefix, header, rows):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filenamePrefix}-{__GetFormattedDate()}.csv"'
    writer = csv.writer(response)
    writer.writerow(header)
    writer.writerows(rows)
    return response


def __PDFResponseGenerator(filenamePrefix, title, template, args):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filenamePrefix}-{__GetFormattedDate()}.pdf"'
    args["title"] = title
    content = render_to_string(template, args)
    HTML(string=content).write_pdf(response)
    return response


def __GetFormattedDate():
    return date.today().strftime("%Y-%m-%d")

def CycleCountHTML(request):
    data = []
    items = map(lambda x: x.getItemDetails(), Item.objects.all().order_by("title"))
    for item in items:
        locations = [{"location": x["name"], "quantity": x["quantity"]} for x in item["locations"]]
        data.append({"name": item["name"], "locations": locations})
    return render(request, 'web/cycle.html', {"items": data})

def CycleCountCSV(request):
    data = []
    items = map(lambda x: x.getItemDetails(), Item.objects.all().order_by("title"))
    for item in items:
        for location in item["locations"]:
            data.append([item["name"], location["name"], location["quantity"]])
    return __CSVResponseGenerator("CycleCount", ["Name", "Location", "Quantity"], data)

def CycleCountPDF(request):
    data = []
    items = map(lambda x: x.getItemDetails(), Item.objects.all().order_by("title"))
    for item in items:
        locations = [{"location": x["name"], "quantity": x["quantity"]} for x in item["locations"]]
        data.append({"name": item["name"], "locations": locations})
    return __PDFResponseGenerator("CycleCount", "Cycle Count", 'pdf/cycle.html', {"items": data})

def InventoryOnHand(request, format=None):
    data = [{"name": x.title, "total": x.totalQuantity} for x in Item.objects.all().order_by("title")]
    if format == "csv":
        return __CSVResponseGenerator("Inventory-on-Hand", ["Name", "Count"], [[x["name"], x["total"]] for x in data])
    elif format == "pdf":
        return __PDFResponseGenerator("Inventory-on-Hand", "Inventory on Hand", 'pdf/onHand.html', {"items": data})
    else:
        return render(request, 'web/onHand.html', {"items": data})
