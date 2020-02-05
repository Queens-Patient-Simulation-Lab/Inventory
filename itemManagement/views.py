from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from itemManagement.models import Item, Location
from simulation_lab import settings


def homePage(request):
    context = {
        'items': [
            item.getItemSummary() for item in Item.objects.all()
        ]
    }

    return render(request, 'itemManagement/homepage.html', context=context)


class ItemDetailsView(TemplateView):
    def get(self, request, itemId, *args, **kwargs):
        isAdmin = False  # TODO, admin check

        print(f"Item ID requested: {itemId}")

        context = Item.objects.get(id=itemId).getItemDetails()
        if isAdmin:
            return render(request, 'itemManagement/item_details_admin.html', context=context)
        else:
            return render(request, 'itemManagement/item_details_assistant.html', context=context)


class LocationView(TemplateView):
    # Displays a page of all item locations.
    def get(self, request, *args, **kwargs):
        locations = Location.objects.filter(deleted=False).all().order_by('name')
        return render(request, 'itemManagement/locationView/locations.html', {'locations': locations})

    """ 
    Handles post requests to the page. If an ID is supplied, it updates an existing location. Otherwise
    it creates a new one. 
    """
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id', "").strip()
        name = request.POST.get('name', "").strip()
        description = request.POST.get('description', "").strip()

        if id != "":
            return self._updateLocation(request, id, name, description)

        if (len(name) < 3):
            messages.error(request, "Name must be at least 3 characters")
            return redirect(request.path_info)

        if (Location.objects.filter(deleted=False, name=name).exists()):
            messages.error(request, "You cannot have two locations with the same name.")
            return redirect(request.path_info)
        try:
            newLocation = Location(name=name, description=description)
            newLocation.save()
            messages.success(request, f"Successfully added '{name}'")

        except IntegrityError as e:  # If a database constraint fails
            print(str(e))
            if getattr(settings, "DEBUG", False):
                messages.error(request, str(e))
            else:
                messages.error(request, "This submission violated the database constraints")

        return redirect(request.path_info)

    # Soft delete a location. We never hard delete locations
    def delete(self, request, id, *args, **kwargs):
        Location.objects.filter(id=id).update(deleted=True)
        messages.success(request, "Successfully deleted")
        return HttpResponse(status=204)  # Return an OK status with no content

    """
    Called  when a request to edit a location is made. Throws an error if the location does not exist
    """

    def _updateLocation(self, request, id, name, description):
        locations = Location.objects.filter(id=id, deleted=False)
        if not locations.exists():
            messages.error(request, "This location does not exist")
            return redirect(request.path_info)
        locations.update(
            name=name,
            description=description
        )
        messages.success(request, "Location modified successfully")
        return redirect(request.path_info)
