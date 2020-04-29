import json
from encodings.base64_codec import base64_decode

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.core.signing import Signer, BadSignature
from django.db import IntegrityError, transaction
from django.db.models import Max
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils import timezone
from django.template.loader import render_to_string

# Create your views here.
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from itemManagement.models import Item, Location, Photo, Tag, ItemStorage
from logs.models import Log
from simulation_lab import settings
from django.templatetags.static import static

from global_login_required import login_not_required


class HomePage(SearchView):
    template_name = "itemManagement/homepage.html"

    def get_queryset(self):
        queryset = super(HomePage, self).get_queryset()
        return queryset.filter(deleted=False)

    def get_context_data(self, *args, **kwargs):
        context = super(HomePage, self).get_context_data(*args, **kwargs)
        print(context)
        objectList = context['object_list']
        # If no results are found, just show the most recently used items
        if (len(objectList) == 0):
            items = [item.getItemSummary() for item in Item.objects.filter(
                deleted=False).order_by('-lastUsed', 'title')]

            # Sadly we can't use the same paginator as Haystack is using for successful queries so we must build our own
            #  an make sure the variables we use are not the same variables used by haystack (e.g use default_items_page instead of page)
            # For more information on using paginators, see https://docs.djangoproject.com/en/3.0/topics/pagination/#using-paginator-in-a-view-functions
            paginator = Paginator(items, 25)
            page_number = context['view'].request.GET.get("default_items_page")
            page_obj = paginator.get_page(page_number)

            context['items'] = page_obj
            context['default_items_page_obj'] = page_obj
        else:
            context['items'] = [item.object.getItemSummary() for item in objectList if item is not None]

        if (len(objectList) == 0 and len(context['query']) != 0):
            messages.warning(self.request, "No results were found. Showing recently used items instead.")
        return context

@login_not_required
def getImage(request, id):
    if not request.user.is_authenticated:
        signer = Signer(sep='?')
        try:
            signer.unsign(request.get_raw_uri())
        except BadSignature:
            raise HttpResponseForbidden
    try:
        photo = Photo.objects.get(pk=id)
    except Photo.DoesNotExist:
        raise Http404
    return HttpResponse(photo.data, content_type=photo.mimeType)


class ItemDeleteView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, itemId, *args, **kwargs):
        item = Item.objects.filter(id=itemId).first()
        itemLocations = ItemStorage.objects.filter(item=item)  # get all locations of the item
        zeroCheck = True
        # the stock of item must be 0 in every location, and cannot be negative
        for location in itemLocations:
            if location.quantity > 0:
                zeroCheck = False
        if zeroCheck:
            item.deleted = True
            item.save(update_fields=['deleted'])
            messages.success(request, f'The item was successfully deleted!')
        else:
            messages.error(request, f'The item stock is not 0. It cannot be  deleted')
        return redirect('homepage')


class ItemDetailsView(TemplateView):
    def get(self, request, itemId, *args, **kwargs):
        isAjax = "X-Requested-With" in request.headers and request.headers["X-Requested-With"] == "XMLHttpRequest"
        isAdmin = request.user.is_superuser
        print(f"Item ID requested: {itemId}")

        if itemId == '':
            context = {"itemId": '', "name": '', "kghId": '', "description": '', "price": '0.00', "unit": '',
                       "totalQuantity": 0, "parLevel": 0, "alertWhenLow": False, 'remainingLocations': Location.objects.all()}
        else:
            context = Item.objects.get(id=itemId).getItemDetails()
            # get all currently unused locations (for purposes of adding new itemStorages)
            locations = Location.objects.exclude(id__in=[x['id'] for x in context['locations']]).all().order_by('name')
            context['remainingLocations'] = locations
        template = 'itemManagement/item_details_admin.html' if isAdmin else 'itemManagement/item_details_assistant.html'

        if isAjax:
            return render(request, template, context=context)
        else:
            return HomePage.as_view(extra_context={'initialModal': render_to_string(template, context=context)})(request, *args, **kwargs)

    def post(self, request, itemId, *args, **kwargs):

        isAdmin = request.user.is_superuser
        itemIsNew = False

        try:
            # Any exceptions that occur or are thrown undo all changes
            with transaction.atomic():

                if isAdmin:
                    if message := itemFormInvalid(request):
                        raise ValueError(message)

                if itemId == '':
                    itemIsNew = True
                    item = Item.objects.create()
                    Log.log(request.user, "Created {item}", item)
                else:
                    item = Item.objects.get(id=itemId)

                item.lastUsed = timezone.now()
                # TODO: item lastUsed updated if decrement clicked

                # Admin Fields updating fields other than quantities if admin
                if isAdmin:
                    # --------TEXT FIELDS--------
                    title = request.POST.get('itemName', "").strip()
                    if item.title != title:
                        item.title = title
                        Log.log(request.user, "Updated {item} changed title to '{string}'", item, title)
                    kghID = request.POST.get('kghId', "").strip()
                    if kghID == "None":
                        kghID = None
                    if item.kghID != kghID:
                        item.kghID = kghID
                        Log.log(request.user, "Updated {item} changed KGH ID to '{string}'", item, kghID)
                    description = request.POST.get('description', "").strip()
                    if item.description != description:
                        item.description = description
                        Log.log(request.user, "Updated {item} changed description to '{string}'", item, description)
                    price = request.POST.get('price', "").strip()
                    if str(item.price) != price:
                        item.price = price
                        Log.log(request.user, "Updated {item} changed price to '{string}'", item, price)
                    unit = request.POST.get('unit', "").strip()
                    if item.unit != unit:
                        item.unit = unit
                        Log.log(request.user, "Updated {item} changed unit to '{string}'", item, unit)
                    alertThreshold = request.POST.get('parLevel', "").strip()
                    if str(item.alertThreshold) != alertThreshold:
                        item.alertThreshold = alertThreshold
                        Log.log(request.user, "Updated {item} changed par level to '{string}'", item, alertThreshold)
                    alertWhenLow = request.POST.get('alertWhenLow', "").strip() == 'on'
                    if item.alertWhenLow != alertWhenLow:
                        item.alertWhenLow = alertWhenLow
                        if alertWhenLow:
                            Log.log(request.user, "Enabled par level alerts on {item}", item)
                        else:
                            Log.log(request.user, "Disabled par level alerts on {item}", item)

                    item.save(update_fields=['title', 'kghID', 'description', 'price', 'unit', 'alertThreshold', 'alertWhenLow'])
                    # ---------------------------
                    deletedImageIds = json.loads(request.POST.get("deletedImageIds"))
                    uploadedImages = json.loads(request.POST.get("uploadedImages"))

                    for i in deletedImageIds:
                        Photo.objects.filter(id=i).delete()
                        Log.log(request.user, "Deleted photo on {item}", item)


                    # Find the highest order element right now so the new image can go after it
                    highestOrderNum = Photo.objects.filter(depicts=item).aggregate(Max("order"))['order__max'] or 0
                    nextOrderNum = highestOrderNum
                    for imageRawData in uploadedImages:
                        nextOrderNum += 1
                        separated = imageRawData.split(";", 1)
                        mimeType = separated[0].replace("data:", "")
                        if (not mimeType.startswith("image/")):
                            raise ValueError("File must be an image")
                        if "base64" not in separated[1]:
                            raise ValueError("File must be base64 encoded")
                        data = urlsafe_base64_decode(separated[1].replace("base64,", "", 1))
                        Photo.objects.create(
                            depicts=item,
                            mimeType=mimeType,
                            data=data,
                            order=nextOrderNum
                        )
                        Log.log(request.user, "Added photo to {item}", item)


                    # --------TAGS-------------
                    newTags = set(request.POST.get('newTags', "").split(','))
                    tagsChanged = set(map(lambda x: x.name, item.tag_set.all())) != newTags
                    if tagsChanged:
                        Log.log(request.user, "Set tags on {item} to '{string}'", item, ", ".join(newTags))
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
                # deletedStorages = list of storages ready to be deleted once POST request happens
                deletedStorages = [int(i) for i in request.POST.getlist('deletedRows') if i != 'undefined']

                for itemStorage in itemStorages:
                    if itemStorage.location.id in deletedStorages:
                        Log.log(request.user, "Deleted storage of {item} at {location}", item, itemStorage.location)
                        itemStorage.delete()
                        continue
                    original_quantity = int(
                        request.POST.get('original-quantity-location-' + str(itemStorage.location.id), "").strip())
                    new_quantity = int(
                        request.POST.get('quantity-location-' + str(itemStorage.location.id), "").strip())
                    diff = new_quantity - original_quantity
                    if diff == 0:
                        continue
                    else:
                        Log.log(request.user, "Set quantity of {item} to {string} (was {string}) at {location}", item, itemStorage.quantity+diff, itemStorage.quantity, itemStorage.location)
                        itemStorage.quantity += diff
                        itemStorage.save()

                newItemStorages = request.POST.getlist('newItemStorage')

                if newItemStorages:
                    for itemStorage in newItemStorages:
                        # quantity of new item
                        quan = request.POST.get('quantity-location-' + str(itemStorage), "").strip()
                        loc = Location.objects.get(id=itemStorage)
                        ItemStorage.objects.create(location=loc, quantity=quan, item=item).save()
                        Log.log(request.user, "Set quantity of {item} to {string} at {location}", item, quan, loc)

                # -------------------------------

                return HttpResponse(status=204)
        except Exception as e:
            print(e)
            context = {"errorMessage": str(e)}
            # Are you certain the user input is the source of the error? would a 500 be more appropriate?
            return HttpResponse(status=400, content=json.dumps(context), content_type='application/json')


def itemFormInvalid(request):
    name = request.POST.get('itemName', "").strip()
    price = request.POST.get('price', "").strip()
    unit = request.POST.get('unit', "").strip()
    kghID = request.POST.get('kghId', "").strip()

    if name == '' or name is None:
        return "Please specify a name"
    if len(name) < 3 or len(name) > 40:
        return "Name must be between 3-40 characters"

    if len(kghID) > 20:
        return "kghID must be maximum 20 characters"

    try:
        "{:.2f}".format(float(price))
    except ValueError:
        return "Price is formatted incorrectly"

    if len(unit) > 20:
        return "Unit must be maximum 20 characters"

    return False


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
