import csv
import traceback
from decimal import Decimal

from django.contrib import messages
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.urls import reverse
from django.utils.encoding import smart_str
from django.views.generic import TemplateView

# TODO, lock down admin only (both get and post request)
from itemManagement.models import Item
from simulation_lab import StringUtils


class KghUploadPage(TemplateView):
    # Keys for dictionary from decode_utf8 saved as variables to avoid misspellings
    ROW_MATERIAL = "material"
    ROW_OLD_MATERIAL = "oldMaterialNumbers"
    ROW_PRICE = "maPrice"

    # Keys for dictionary of changes passed to context
    CHANGE_TITLE = "title"
    CHANGE_KGH_ID = "kghId"
    CHANGE_OLD_KGH_ID = "oldKghId"
    CHANGE_OLD_PRICE = "oldPrice"
    CHANGE_NEW_PRICE = "newPrice"

    # [kghId, title, oldKghId, oldPrice, newPrice]

    def get(self, request, *args, **kwargs):
        return render(request, 'kghDataManagement/kgh_upload_page.html')

    def post(self, request, *args, **kwargs):
        # Note, if this is slow, we can parallelize this
        try:
            kghFile = request.FILES['kghFile'] or None

            if kghFile is None or not kghFile.name.endswith('.csv'):
                messages.error(request, 'Error: File must be CSV type.')
                return redirect('kgh-upload')

            reader = self.decode_utf8(kghFile)

            # Lazy query for all Items that  have a non-empty kghID and are not deleted
            allKghItems = Item.objects \
                .exclude(kghID__isnull=True) \
                .exclude(kghID__exact='') \
                .filter(deleted=False) \
                .all()
            # Convert allKghItems to dictionary for fast comparisons
            kghIdDict = {x.kghID: x for x in allKghItems}

            with transaction.atomic():  # If any errors propagate, rollback all changes
                changes = []  # List of all changes made for the Context
                for row in reader:
                    kghItem = kghIdDict.get(row.get(self.ROW_MATERIAL))

                    if kghItem is not None:  # If an Item has the material number
                        change = self.handleItemPriceChange(row, kghItem)
                        # If a change was made
                        if (len(change) != 0):
                            change[self.CHANGE_KGH_ID] = kghItem.kghID
                            changes.append(change)

                    # If an item matches an old KGH item ID
                    elif (kghItem := self.getItemMatchingOldIds(row.get(self.ROW_OLD_MATERIAL), kghIdDict)) is not None:
                        change = self.handleItemPriceChange(row, kghItem)

                        title = kghItem.title
                        newKghId = row.get(self.ROW_MATERIAL)

                        change[self.CHANGE_TITLE] = title
                        change[self.CHANGE_KGH_ID] = newKghId

                        kghItem.kghID = newKghId

                        changes.append(change)

                Item.objects.bulk_update(list(kghIdDict.values()), ["kghID", "price"])
        except IntegrityError as e:
            messages.error(request, f"Error: {str(e)}")
            traceback.print_exc()
            return redirect('kgh-upload')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            traceback.print_exc()
            return redirect('kgh-upload')

        messages.success(request, "File upload successful")
        context = {
            "changes": changes,
            "catalogUploaded": True
        }
        #  TODO, make a table of all changes (context already provided)
        # If no changes are made, let the user know
        # Use the global keys to reference each field

        return render(request, 'kghDataManagement/kgh_upload_page.html', context=context)

    # row: A row (as a dictionary) of the KGH catalog, as parsed from decode_utf8()
    # kghItem: An [Item] that has a valid KGH ID (either outdated or present)
    # Updates kghItem price and returns a dictionary of the changes made for the response context
    def handleItemPriceChange(self, row, kghItem):
        newPriceString = row.get(self.ROW_PRICE).strip()
        newPrice = StringUtils.getFloatOrNone(newPriceString)
        if newPrice == None:
            raise Exception(
                f"Could not parse material price for item with KGH ID: {kghItem.kghID}. Please make sure it is a decimal with no non-digit characters.")
        oldPrice = kghItem.price
        if float(oldPrice) != newPrice:
            kghItem.price = newPrice
            return ({
                self.CHANGE_TITLE: kghItem.title,
                self.CHANGE_OLD_PRICE: oldPrice,
                self.CHANGE_NEW_PRICE: newPrice,
                self.CHANGE_OLD_KGH_ID: kghItem.kghID
            })
        return {}

    # oldIds: A space separated string of old KGH IDs
    # itemDictionary: itemDictionary[kghID] == Item
    def getItemMatchingOldIds(self, oldIds, itemDictionary):
        ids = oldIds.split(" ")
        for oldId in ids:
            item = itemDictionary.get(oldId)
            if item is not None:
                return item

    # Generator that decodes one row of the csv at a time
    # Returns a value when iterated on, this way we don't need to store the entire decryption in memory
    def decode_utf8(self, file):
        # Skip the first row of the file which is the header
        iterator = iter(file)
        next(iterator)
        for line in iterator:
            row = line.decode('utf-8').replace('\r\n', '').split(',')
            yield {
                self.ROW_MATERIAL: row[0],
                # "materialDescription": row[1],
                # "un": row[2],
                self.ROW_OLD_MATERIAL: row[3],
                # Index four and five are blank
                # "matlGrp": row[6],
                # "basicMaterial": row[7],
                # "type": row[8],
                self.ROW_PRICE: row[9]
                # "currency": row[10]
            }


# TODO Admin Check
def downloadKghTemplate(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="KGH Catalog Template.csv"'

    with open("kghDataManagement/kghCatalogTemplate.csv") as file:
        reader = csv.reader(file)
        writer = csv.writer(response)
        writer.writerows(reader)

    return response