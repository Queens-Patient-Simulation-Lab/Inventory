import csv

from django.contrib import messages
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

# TODO, lock down admin only (both get and post request)
class KghUploadPage(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'kghDataManagement/kgh_upload_page.html')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Note, if this is slow, we can parallelize this
        try:
            kghFile = request.FILES['kghFile'] or None

            if kghFile is None or not kghFile.name.endswith('.csv'):
                messages.error(request, 'Error: File must be CSV type.')
                return redirect('kgh-upload')
            # TODO, handle if file too large

            reader = self.decode_utf8(kghFile)

            with transaction.atomic(): # If any errors propogate, rollback all changes
                for line in reader:
                    print(line)

        except IntegrityError as e:
            print(f"Error: {e.message}")
            messages.error(request, f"Error: {e.message}")
            return redirect('kgh-upload')
        except Exception as e:
            print("Error: Something went wrong")
            messages.error(request, "Error: Something went wrong")
            return redirect('kgh-upload')




        # Make method transactional
        # Get csv, confirm right format
        # Load all database ID's into some form of dictionary
        # Check material number of each row against dictionary
            # Update price field if found
        # check oldmaterial number of each row against dictionary
            #Update price and id if found


        # If there are any items with wrong ID's (not in spreadsheet), give warning. Multiple ways
            # 1. At the end, check that database id's are a subset of material ID's
            # 2. After each item is updated, remove item from dictionary

        #Show table of changes (or lack thereof)


        messages.success(request,"HI")
        return redirect('kgh-upload')

    # Generator that decodes one line of the csv at a time
    # Returns a value when iterated on, this way we don't need to store the entire decryption in memory
    def decode_utf8(self, file):
        for line in file:
            yield line.decode('utf-8').replace('\r\n','').split(',')