from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from itemManagement.models import Item, Location, ItemStorage, Photo
from simulation_lab import settings


def homePage(request):
    context = {
        'items': [
            item.getItemSummary() for item in Item.objects.all()
        ]
    }

    return render(request, 'itemManagement/homepage.html', context=context)


def sampleItem(request, itemId):
    print(f"Item ID requested: {itemId}")

    context = Item.objects.get(id=itemId).getItemDetails()
    return render(request, 'itemManagement/item_details.html', context=context)


class LocationView(TemplateView):
    def get(self, request, *args, **kwargs):
        locations = Location.objects.filter(deleted=False).all().order_by('name')
        return render(request, 'itemManagement/locations.html', {'locations': locations})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', "").strip()
        description = request.POST.get('description', "").strip()

        if (len(name) < 3):
            messages.error(request, "Name must be at least 3 characters")
            return redirect("location-list")

        if (Location.objects.filter(deleted=False, name=name).exists()):
            messages.error(request, "You cannot have two locations with the same name.")
            return redirect("location-list")
        try:
            newLocation = Location(name=name, description=description)
            newLocation.save()
            messages.success(request, f"Successfully added '{name}'")

        except IntegrityError as e:
            print(str(e))
            if getattr(settings, "DEBUG", False):
                messages.error(request, str(e))
            else:
                messages.error("This submission violated the database constraints")

        return redirect("location-list")

        return self.get(request)

    def delete(self, request, id, *args, **kwargs):
        Location.objects.filter(id=id).update(deleted=True)
        messages.success(request, "Successfully deleted")
        return self.get(request, *args, **kwargs)
