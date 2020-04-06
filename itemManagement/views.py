from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

# Create your views here.
from django.views.generic import TemplateView
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from itemManagement.models import Item, Location, Photo, Tag, ItemStorage
from simulation_lab import settings
from django.templatetags.static import static



class HomePage(SearchView):
    template_name = "itemManagement/homepage.html"

    def get_queryset(self):
        queryset = super(HomePage, self).get_queryset()
        return queryset.filter(deleted=False).order_by('-lastUsed')

    def get_context_data(self, *args, **kwargs):
        context = super(HomePage, self).get_context_data(*args, **kwargs)
        print(context)
        objectList = context['object_list']
        if (len(objectList) == 0):
            context['items'] = [item.getItemSummary() for item in Item.objects.filter(
                deleted=False).order_by('-lastUsed', 'title')[:20]]
        else:
            context['items'] = [item.object.getItemSummary() for item in objectList]

        if (len(objectList) == 0 and len(context['query']) != 0):
            messages.warning(self.request, "No results were found. Showing recently used items instead.")
        return context


def getImage(request, id):
    try:
        photo = Photo.objects.get(pk=id)
    except Photo.DoesNotExist:
        raise Http404
    return HttpResponse(photo.data, content_type=photo.mimeType)


class ItemDetailsView(TemplateView):
    def get(self, request, itemId, *args, **kwargs):
        isAdmin = request.user.is_superuser

        print(f"Item ID requested: {itemId}")

        context = Item.objects.get(id=itemId).getItemDetails()

        if isAdmin:
            return render(request, 'itemManagement/item_details_admin.html', context=context)
        else:
            return render(request, 'itemManagement/item_details_assistant.html', context=context)

    def post(self, request, itemId, *args, **kwargs):

        item = Item.objects.get(id=itemId)

        item.lastUsed = timezone.now()
        # TODO: item lastUsed updated if decrement clicked

        isAdmin = request.user.is_superuser

        # Admin Fields updating fields other than quantities if admin
        if isAdmin:
            # --------TEXT FIELDS--------
            item.title = request.POST.get('itemName', "").strip()
            item.description = request.POST.get('description', "").strip()
            item.price = request.POST.get('price', "").strip()
            item.unit = request.POST.get('unit', "").strip()
            item.save(update_fields=['title', 'description', 'price', 'unit'])
            # ---------------------------

            # --------TAGS-------------
            newTags = request.POST.get('newTags', "").split(',')
            # clear all tags
            item.tag_set.all().delete()
            # add back all new edited tags
            for newTag in newTags:
                if newTag != "" and newTag is not None:
                    newTag = Tag.objects.create(name=newTag.strip(), item=item)
                    newTag.save()
            # -------------------------
        # END if isAdmin

        # ----Item storage quantities at each location----
        # itemStorages list of ItemStorage objects where the item is the current item form
        itemStorages = ItemStorage.objects.filter(item=item)

        for itemStorage in itemStorages:
            original_quantity = int(request.POST.get('original-quantity-location-' + str(itemStorage.location.id), "").strip())
            new_quantity = int(request.POST.get('quantity-location-' + str(itemStorage.location.id), "").strip())
            diff = new_quantity - original_quantity
            itemStorage.quantity += diff
            itemStorage.save()
        # -------------------------------

        # TODO: Post Images

        # TODO: Input validation

        # TODO: Return to homepage with same previous state after POST
        return HttpResponse(status=204)


class LocationView(UserPassesTestMixin, TemplateView):

    def test_func(self):
        return self.request.user.is_superuser

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
        location = Location.objects.get(id=id)
        if location is None:
            messages.error(request, "ID did not match any locations")
            return HttpResponse(status=400)
        if location.itemstorage_set.filter(quantity__gt=0).exists():  # If this location has an item with >0 quantity
            messages.error(request, "You can't delete a location that is holding items")
            return HttpResponse(status=400)
        location.deleted = True
        location.save()
        messages.success(request, "Successfully deleted")
        return HttpResponse(status=204)  # Return an OK status with no content

    """
    Called  when a request to edit a location is made. Throws an error if the location does not exist
    """

    def _updateLocation(self, request, id, name, description):
        location = Location.objects.filter(id=id).first()
        if location is None or location.deleted:
            messages.error(request, "This location does not exist")
            return redirect(request.path_info)
        if (len(name) < 3):
            messages.error(request, "Name must be at least 3 characters")
            return redirect(request.path_info)

        if (name != location.name and Location.objects.filter(deleted=False, name=name).exists()):
            messages.error(request, "You cannot have two locations with the same name.")
            return redirect(request.path_info)

        location.name = name
        location.description = description
        location.save()
        messages.success(request, "Location modified successfully")
        return redirect(request.path_info)
