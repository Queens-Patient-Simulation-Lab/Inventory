from django.urls import path, re_path

from itemManagement.views import LocationView, ItemDetailsView, HomePage
from . import views

URL_LOCATION_LIST = "location-list"

URL_HOMEPAGE = "homepage"

URL_ITEM_DETAILS = "item-details"

URL_GET_PHOTO = "get-photo"

urlpatterns = [
    re_path(r'^item/(?P<itemId>.*)?$', ItemDetailsView.as_view(), name=URL_ITEM_DETAILS),
    path('home/', HomePage.as_view(), name=URL_HOMEPAGE),
    path('locations/', LocationView.as_view(), name=URL_LOCATION_LIST),
    path('locations/<int:id>/', LocationView.as_view(), name=URL_LOCATION_LIST),
    path("image/<int:id>", views.getImage, name=URL_GET_PHOTO)
]
