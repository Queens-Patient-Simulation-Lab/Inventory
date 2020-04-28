import csv
import io
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from itemManagement.models import Item
from django.http import FileResponse, HttpResponse
from datetime import date
from weasyprint import HTML
from django.utils import timezone
from emails.email import EmailManager
from itemManagement.models import Item
from logs.models import Log
from security.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from itertools import chain
from django.urls import reverse



@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def CycleCountHTML(request):
    data = []
    items = map(lambda x: x.getItemDetails(), Item.objects.all().order_by("title").filter(deleted=False))
    for item in items:
        locations = [{"location": x["name"], "quantity": x["quantity"]} for x in item["locations"]]
        data.append({"name": item["name"], "id": item["itemId"], "locations": locations})
    return render(request, 'web/cycle.html', {"items": data})

@user_passes_test(lambda u: u.is_superuser)
def CycleCountCSV(request):
    data = []
    items = map(lambda x: x.getItemDetails(), Item.objects.all().order_by("title").filter(deleted=False))
    for item in items:
        for location in item["locations"]:
            data.append([item["name"], location["name"], location["quantity"]])
    return __CSVResponseGenerator("CycleCount", ["Name", "Location", "Quantity"], data)

@user_passes_test(lambda u: u.is_superuser)
def CycleCountPDF(request):
    data = []
    items = map(lambda x: x.getItemDetails(), Item.objects.all().order_by("title").filter(deleted=False))
    for item in items:
        locations = [{"location": x["name"], "quantity": x["quantity"]} for x in item["locations"]]
        data.append({"name": item["name"], "locations": locations})
    return __PDFResponseGenerator("CycleCount", "Cycle Count", 'pdf/cycle.html', {"items": data})

@user_passes_test(lambda u: u.is_superuser)
def InventoryOnHand(request, format=None):
    data = [{"id": x.id, "name": x.title, "total": x.totalQuantity} for x in Item.objects.all().order_by("title").filter(deleted=False)]
    if format == "csv":
        return __CSVResponseGenerator("Inventory-on-Hand", ["Name", "Count"], [[x["name"], x["total"]] for x in data])
    elif format == "pdf":
        return __PDFResponseGenerator("Inventory-on-Hand", "Inventory on Hand", 'pdf/onHand.html', {"items": data})
    else:
        return render(request, 'web/onHand.html', {"items": data})

@user_passes_test(lambda u: u.is_superuser)
def InventoryObsolescence(request, format=None):
    data = [{"id": x.id, "name": x.title, "lastUsed": x.lastUsed} for x in Item.objects.filter(deleted=False).filter(lastUsed__lte=timezone.now() - timezone.timedelta(days=365)).order_by("title")]
    if format == "csv":
        return __CSVResponseGenerator("inventory-obsolescence", ["Name", "Last Used"], [[x["name"], x["lastUsed"]] for x in data])
    elif format == "pdf":
        return __PDFResponseGenerator("inventory-obsolescence", "Inventory Obsolescence", 'pdf/obsolescence.html', {"items": data})
    else:
        return render(request, 'web/obsolescence.html', {"items": data})

@user_passes_test(lambda u: u.is_superuser)
def ReorderList(request, format=None):
    items = Item.objects.all().order_by("title").filter(deleted=False)
    belowThreshold = filter(lambda x: x.needToNotifyAdmin(), items)
    data = [{"id": x.id, "name": x.title, "total": x.totalQuantity, "par": x.alertThreshold, "kghID": x.kghID} for x in belowThreshold]
    if format == "csv":
        return __CSVResponseGenerator("reorder", ["Name", "KGH ID", "Current Total", "Par Level"], [[x["name"], x["kghID"], x["total"], x["par"]] for x in data])
    elif format == "pdf":
        return __PDFResponseGenerator("reorder", "Reorder List", 'pdf/reorder.html', {"items": data})
    else:
        return render(request, 'web/reorder.html', {"items": data})

@user_passes_test(lambda u: u.is_superuser)
def InventoryValuation(request, format=None):
    data = [{"id": x.id, "name": x.title, "quantity": x.totalQuantity, "price": x.price, "value": x.totalQuantity * x.price} for x in Item.objects.all().filter(deleted=False)]
    data.sort(key=lambda x: x["value"], reverse=True)
    total = sum(map(lambda x: x["value"], data))
    if format == "csv":
        return __CSVResponseGenerator("valuation", ["Name", "Quantity", "Price", "Value"], [[x["name"], x["quantity"], x["price"], x["value"]] for x in data])
    elif format == "pdf":
        return __PDFResponseGenerator("valuation", "Inventory Valuation", 'pdf/valuation.html', {"items": data, "total": total})
    else:
        return render(request, 'web/valuation.html', {"items": data, "total": total})


@user_passes_test(lambda u: u.is_superuser)
def ItemHistory(request, itemID, format=None):
    item = Item.objects.get(pk=itemID)
    data = Log.get_logs_for_item(item)
    if format == "csv":
        return __CSVResponseGenerator("item_history", ["Time", "User", "Action"], [[str(x.time), x.user.name, x.to_string()] for x in data])
    elif format == "pdf":
        return __PDFResponseGenerator("item_history", "Item History " + item.title, 'pdf/itemHistory.html', {"item": item, "logs": data})
    else:
        rich = map(lambda x: {"time": x.time.strftime("%Y-%m-%d %I:%M %p"), "user": x.user.name, "action": x.to_string(
            lambda item: f"<a href=\"{reverse('item-details', args=(item.id,))}\">{item.title}</a>"
        )}, data)
        return render(request, 'web/itemHistory.html', {"item": item, "logs": rich})


@user_passes_test(lambda u: u.is_superuser)
def UserHistory(request):
    isAjax =  "X-Requested-With" in request.headers and request.headers["X-Requested-With"] == "XMLHttpRequest"
    format = request.GET.get('format', None)
    user = request.GET.get('user', None)
    if format not in {"csv", "pdf", None}:
        messages.error(request, "Invalid report format '" + format + "'")
        return redirect("user-history")
    if format != None and user == None:
        messages.error(request, "Custom formats require a target user")
        return redirect("user-history")
    if isAjax and user == None:
        messages.error(request, "Ajax requests require a target user")
        return redirect("user-history")

    if not isAjax:
        if format == None:
            return render(request, 'web/userHistory.html', {"users": User.objects.all(), "initalSelectedUser": user})

    if user == "all":
        data = Log.objects.all()
    else:
        data = Log.get_logs_for_user(User.objects.get(pk=user))
    if not isAjax:
        if format == "csv":
             return __CSVResponseGenerator("user-history", ["Time", "User", "Action"], [[str(x.time), x.user.name, x.to_string()] for x in data])
        return __PDFResponseGenerator("user-history", "User History", 'pdf/userHistory.html', {"histories": data})
    rich = map(lambda x: {"time": x.time.strftime("%Y-%m-%d %I:%M %p"), "user": x.user.name, "action": x.to_string(
        lambda item: f"<a href=\"{reverse('item-details', args=(item.id,))}\">{item.title}</a>"
    )}, data)
    return render(request, 'web/userHistoryData.html', {"histories": rich})
