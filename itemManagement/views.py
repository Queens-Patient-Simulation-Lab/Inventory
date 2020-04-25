import json
from encodings.base64_codec import base64_decode

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Max
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.template.loader import render_to_string

# Create your views here.
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from itemManagement.models import Item, Location, Photo, Tag, ItemStorage
from logs.models import  ItemCountLogs, ItemInfoLogs, LOGCODE_CHANGEITEM, LOGMSG_CHANGEITEM, LOGCODE_STOCKCHANGE, \
    LOGMSG_STOCKCHANGE, LOGCODE_CREATEITEM, LOGMSG_CREATEITEM, LOGCODE_DELETEITEM, LOGMSG_DELETEITEM
from simulation_lab import settings
from django.templatetags.static import static



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


def getImage(request, id):
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
        isAjax =  "X-Requested-With" in request.headers and request.headers["X-Requested-With"] == "XMLHttpRequest"
        isAdmin = request.user.is_superuser
        print(f"Item ID requested: {itemId}")

        if itemId == '':
            context = {"itemId": '', "name": '', "kghId": '', "description": '', "price": '0.00', "unit": '', "totalQuantity": 0}
        else:
            context = Item.objects.get(id=itemId).getItemDetails()
        template = 'itemManagement/item_details_admin.html' if isAdmin else 'itemManagement/item_details_assistant.html'
        if isAjax:
            return render(request, template, context=context)
        else:
            return HomePage.as_view(extra_context={'initialModal': render_to_string(template, context=context)})(request, *args, **kwargs)

    def post(self, request, itemId, *args, **kwargs):

        if message := itemFormInvalid(request):
            messages.error(request, message)
            return HttpResponse(status=400)

        itemIsNew = False

        try:
            # Any exceptions that occur or are thrown undo all changes
            with transaction.atomic():

                if itemId == '':
                    itemIsNew = True
                    item = Item.objects.create()
                    ItemInfoLogs.logging(request.user, item, LOGCODE_CREATEITEM, LOGMSG_CREATEITEM, kghID=item.kghID,
                                         price=item.price, *args, **kwargs)
                else:
                    item = Item.objects.get(id=itemId)

                item.lastUsed = timezone.now()
                # TODO: item lastUsed updated if decrement clicked

                isAdmin = request.user.is_superuser

                # Admin Fields updating fields other than quantities if admin
                if isAdmin:
                    # --------TEXT FIELDS--------
                    item.title = request.POST.get('itemName', "").strip()
                    item.kghID = request.POST.get('kghId', "").strip()
                    item.description = request.POST.get('description', "").strip()
                    item.price = request.POST.get('price', "").strip()
                    item.unit = request.POST.get('unit', "").strip()
                    item.save(update_fields=['title', 'kghID', 'description', 'price', 'unit'])
                    # ---------------------------
                    deletedImageIds = json.loads(request.POST.get("deletedImageIds"))
                    uploadedImages = json.loads(request.POST.get("uploadedImages"))

                    for i in deletedImageIds:
                        Photo.objects.filter(id=i).delete()

                    # Find the highest order element right now so the new image can go after it
                    highestOrderNum = Photo.objects.filter(depicts=item).aggregate(Max("order"))['order__max'] or 0
                    nextOrderNum = highestOrderNum
                    for imageRawData in uploadedImages:
                        nextOrderNum += 1
                        separated = imageRawData.split(";", 1)
                        mimeType = separated[0].replace("data:","")
                        if (not mimeType.startswith("image/")):
                            raise ValueError("File must be an image")
                        if "base64" not in separated[1]:
                            raise ValueError("File must be base64 encoded")
                        data = urlsafe_base64_decode(separated[1].replace("base64,","", 1))
                        Photo.objects.create(
                            depicts=item,
                            mimeType=mimeType,
                            data=data,
                            order=nextOrderNum
                        )

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
                    if not itemIsNew:
                        ItemInfoLogs.logging(request.user, item, LOGCODE_CHANGEITEM, LOGMSG_CHANGEITEM, item.kghID,
                                         item.price)


                # END if isAdmin

                # ----Item storage quantities at each location----
                # itemStorages list of ItemStorage objects where the item is the current item form
                itemStorages = ItemStorage.objects.filter(item=item)

                for itemStorage in itemStorages:
                    original_quantity = int(request.POST.get('original-quantity-location-' + str(itemStorage.location.id), "").strip())
                    new_quantity = int(request.POST.get('quantity-location-' + str(itemStorage.location.id), "").strip())
                    diff = new_quantity - original_quantity
                    if diff == 0:
                        pass
                    else:
                        itemStorage.quantity += diff
                        itemStorage.save()
                        ItemCountLogs.logging(request.user, item, itemStorage.quantity, itemStorage.location,
                                              LOGCODE_STOCKCHANGE, LOGMSG_STOCKCHANGE)

                # -------------------------------

                # TODO: Post Images

                # TODO: Input validation

                # TODO: Return to homepage with same previous state after POST
                return HttpResponse(status=204)
        except Exception as e:
            print(e)
            context = {"errorMessage": str(e)}
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
