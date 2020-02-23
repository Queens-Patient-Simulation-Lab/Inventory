import csv
import traceback

from django.contrib import messages
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect

# Create your views here.
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
                        if (len(change) is not 0):
                            change[self.CHANGE_KGH_ID] = kghItem.kghID
                            changes.append(change)

                    elif (kghItem := self.getItemMatchingOldIds(row.get(self.ROW_OLD_MATERIAL), kghIdDict)) is not None:
                        change = self.handleItemPriceChange(row, kghItem)


                        title = kghItem.title
                        oldKghId = kghItem.kghID
                        newKghId = row.get(self.ROW_MATERIAL)

                        change[self.CHANGE_TITLE] = title
                        change[self.CHANGE_OLD_KGH_ID] = oldKghId
                        change[self.CHANGE_KGH_ID] = newKghId

                        kghItem.kghID = newKghId

                Item.objects.bulk_update(list(kghIdDict.values()), ["kghID", "price"])
        except IntegrityError as e:
            messages.error(request, f"Error: {str(e)}")
            traceback.print_exc()
            return redirect('kgh-upload')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            traceback.print_exc()
            return redirect('kgh-upload')


        # If there are any items with wrong ID's (not in spreadsheet), give warning. Multiple ways
        # 1. At the end, check that database id's are a subset of material ID's
        # 2. After each item is updated, remove item from dictionary

        # Show table of changes (or lack thereof)

        messages.success(request, "File upload successful")
        context = {
            "changes": changes
        }
        return render(request, 'kghDataManagement/kgh_upload_page.html', context=context)

    def handleItemPriceChange(self, row, kghItem):
        newPriceString = row.get(self.ROW_PRICE).strip()
        newPrice = StringUtils.getFloatOrNone(newPriceString)
        if (newPrice != None):
            oldPrice = kghItem.price
            if oldPrice != newPrice:
                kghItem.price = float(newPrice)
                return ({
                    self.CHANGE_TITLE: kghItem.title,
                    self.CHANGE_OLD_PRICE: oldPrice,
                    self.CHANGE_NEW_PRICE: newPrice
                })
        return {}

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
